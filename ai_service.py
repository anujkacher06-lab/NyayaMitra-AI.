import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT_EN = """You are NyayaMitra, an Indian legal-information assistant.
You provide general legal information, not professional legal advice.
Use only the supplied verified context.
Do not invent:
- law names
- legal sections
- deadlines
- court decisions
- helpline numbers
- government portals

If the verified context does not contain enough information, say:
"I do not have enough verified information to answer this safely."

Respond using this strict structure:
1. Problem category
2. Simple explanation
3. Immediate actions
4. Documents and evidence
5. Official resources
6. When professional help is needed
7. Disclaimer

Important guidelines:
- Never cite the old Indian Penal Code (IPC) as current law. Use the Bharatiya Nyaya Sanhita (BNS), 2023, which came into force on July 1, 2024.
- Do not guarantee any legal outcome or claim the user will win a case.
- Keep the language clear, empathetic, and actionable for ordinary Indian citizens.
- Return your answer in valid JSON matching the requested schema.
"""

SYSTEM_PROMPT_HI = """आप 'न्यायमित्र' (NyayaMitra) हैं - एक भारतीय कानूनी सूचना सहायक।
आप सामान्य कानूनी जानकारी प्रदान करते हैं, पेशेवर कानूनी सलाह नहीं।
केवल दिए गए सत्यापित संदर्भ (Verified Context) का ही उपयोग करें।
अपनी तरफ से कोई फर्जी कानून, पुरानी धाराएं, हेल्पलाइन नंबर या सरकारी पोर्टल न बनाएं।

पुराने भारतीय दंड संहिता (IPC) के स्थान पर भारतीय न्याय संहिता (BNS), 2023 का ही उल्लेख करें।
किसी भी कानूनी नतीजे या जीत की गारंटी न दें।

निम्न निश्चित संरचना में उत्तर दें:
1. समस्या की श्रेणी
2. सरल व्याख्या
3. तत्काल आवश्यक कदम
4. जरूरी दस्तावेज और साक्ष्य सूची
5. आधिकारिक सरकारी संसाधन व हेल्पलाइन
6. पेशेवर कानूनी सहायता कब लें
7. सुरक्षा अस्वीकरण
"""

def generate_fallback_response(category: str, question: str, verified_ctx: dict, language: str) -> dict:
    """
    Offline / zero-API-key deterministic fallback that strictly formats 
    the verified JSON context into the standard structured response.
    Guarantees the system works seamlessly even without an external API key.
    """
    lang_code = verified_ctx.get("lang_code", "en")
    is_hi = (lang_code == "hi")

    if is_hi:
        help_needed = (
            "यदि मामला ₹5,00,000 से अधिक की धोखाधड़ी का हो, या नियोक्ता/कंपनी द्वारा निरंतर उत्पीड़न "
            "अथवा धमकी दी जा रही हो, तो नालसा (NALSA) के निःशुल्क विधिक सेवा वकील या टेली-लॉ (Tele-Law) से तत्काल संपर्क करें।"
        )
        disclaimer = (
            "महत्वपूर्ण अस्वीकरण: यह केवल सामान्य कानूनी जानकारी और प्रक्रियात्मक मार्गदर्शन है, "
            "कोई पेशेवर कानूनी सलाह नहीं। किसी भी औपचारिक कानूनी कार्रवाई से पहले योग्य अधिवक्ता या विधिक सेवा प्राधिकरण से परामर्श करें।"
        )
    else:
        help_needed = (
            "Seek formal legal counsel or free legal aid via NALSA / Tele-Law if the financial loss exceeds ₹5,00,000, "
            "involves complex multi-jurisdictional fraud, criminal intimidation, or complete non-cooperation from the opposite party."
        )
        disclaimer = (
            "Important Safety Disclaimer: This is general legal information and procedural guidance, not professional legal advice. "
            "NyayaMitra does not guarantee any legal outcome. Always verify specifics with certified legal counsel or District Legal Services Authority (DLSA)."
        )

    return {
        "category": verified_ctx.get("title", category),
        "explanation": verified_ctx.get("explanation", ""),
        "actions": verified_ctx.get("actions", []),
        "evidence": verified_ctx.get("evidence", []),
        "applicable_laws": verified_ctx.get("applicable_laws", []),
        "official_resources": verified_ctx.get("resources", []),
        "when_professional_help_needed": help_needed,
        "disclaimer": disclaimer,
        "verified_date": verified_ctx.get("verified_date", "2026-07-16"),
        "generation_mode": "verified_knowledge_engine"
    }

def query_gemini_api(api_key: str, system_prompt: str, user_content: str) -> str:
    # Use Gemini REST API
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": f"{system_prompt}\n\nUser Question and Verified Context:\n{user_content}"}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json"
        }
    }
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, json=payload, headers=headers, timeout=12)
    if resp.status_code == 200:
        data = resp.json()
        candidates = data.get("candidates", [])
        if candidates:
            return candidates[0]["content"]["parts"][0]["text"]
    raise Exception(f"Gemini API returned status {resp.status_code}: {resp.text}")

def query_openai_api(api_key: str, system_prompt: str, user_content: str) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"}
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=12)
    if resp.status_code == 200:
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    raise Exception(f"OpenAI API returned status {resp.status_code}: {resp.text}")

def generate_legal_response(category: str, question: str, verified_ctx: dict, language: str = "English") -> dict:
    """
    RAG-Safe Response Generator:
    1. Prepares strict system prompt and verified context.
    2. Calls Gemini or OpenAI if API key available.
    3. Validates structure. If external call fails or API key absent, smoothly falls back to verified RAG engine.
    """
    lang_code = verified_ctx.get("lang_code", "en")
    is_hi = (lang_code == "hi")
    system_prompt = SYSTEM_PROMPT_HI if is_hi else SYSTEM_PROMPT_EN

    user_content = f"""
USER QUESTION:
"{question}"

PREFERRED LANGUAGE: {language}

STRICT VERIFIED CONTEXT FROM INDIA CODE & NATIONAL PORTALS:
Category: {verified_ctx.get('title')}
Applicable Legislation: {json.dumps(verified_ctx.get('applicable_laws', []), ensure_ascii=False)}
Explanation Baseline: {verified_ctx.get('explanation')}
Immediate Action Guidance: {json.dumps(verified_ctx.get('actions', []), ensure_ascii=False)}
Evidence Checklist: {json.dumps(verified_ctx.get('evidence', []), ensure_ascii=False)}
Official Helplines and Portals: {json.dumps(verified_ctx.get('resources', []), ensure_ascii=False)}

Please structure the final response tailored to the user's situation using ONLY the facts above in JSON format with these exact keys:
{{
  "category": "{verified_ctx.get('title')}",
  "explanation": "concise explanation directly addressing user's situation",
  "actions": ["step 1", "step 2", "step 3", "step 4"],
  "evidence": ["doc 1", "doc 2", "doc 3"],
  "official_resources": [list of relevant resources],
  "applicable_laws": [laws from context],
  "when_professional_help_needed": "clear threshold when to engage an advocate",
  "disclaimer": "safety disclaimer"
}}
"""

    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("AI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    ai_text = None
    if gemini_key:
        try:
            ai_text = query_gemini_api(gemini_key, system_prompt, user_content)
        except Exception as e:
            print(f"[Warning] Gemini API call error: {e}")

    if not ai_text and openai_key:
        try:
            ai_text = query_openai_api(openai_key, system_prompt, user_content)
        except Exception as e:
            print(f"[Warning] OpenAI API call error: {e}")

    if ai_text:
        try:
            # Parse JSON
            cleaned = ai_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            parsed = json.loads(cleaned.strip())
            
            # Ensure mandatory fields
            parsed["category"] = parsed.get("category") or verified_ctx.get("title")
            parsed["actions"] = parsed.get("actions") or verified_ctx.get("actions")
            parsed["evidence"] = parsed.get("evidence") or verified_ctx.get("evidence")
            parsed["official_resources"] = verified_ctx.get("resources") # Always keep authoritative official resources
            parsed["applicable_laws"] = verified_ctx.get("applicable_laws")
            parsed["verified_date"] = verified_ctx.get("verified_date")
            parsed["generation_mode"] = "ai_augmented_rag"
            return parsed
        except Exception as e:
            print(f"[Warning] Failed to parse AI JSON response: {e}, falling back to verified RAG")

    # Safe deterministic fallback
    return generate_fallback_response(category, question, verified_ctx, language)

def generate_follow_up_answer(category: str, original_question: str, follow_up_question: str, verified_ctx: dict, language: str = "English") -> str:
    """
    Answers conversational follow-up questions from citizens grounded in verified laws.
    """
    is_hi = language.lower().startswith("hi")
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("AI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    system_prompt = (
        "You are NyayaMitra AI, an Indian legal information assistant. "
        "Answer the citizen's follow-up question concisely (max 3-4 bullet points), grounded in Indian law (BNS 2023, BNSS 2023, CPA 2019, RTI 2005). "
        "Never invent laws or citation numbers. Always advise consulting DLSA/NALSA (15100) or Tele-Law (14488) for professional counsel."
        if not is_hi else
        "आप न्यायमित्र (NyayaMitra AI) हैं। नागरिक के अनुवर्ती (follow-up) प्रश्न का संक्षिप्त और स्पष्ट उत्तर 3-4 बिंदुओं में दें। "
        "उत्तर भारतीय कानून (BNS 2023, BNSS 2023, CPA 2019, RTI 2005) पर आधारित होना चाहिए। "
        "नालसा (15100) या टेली-लॉ (14488) से विधिक परामर्श लेने का सुझाव दें।"
    )

    user_prompt = f"""Case Category: {category}
Original Citizen Problem: {original_question}
Follow-up Question: {follow_up_question}
Verified Statutes: {json.dumps(verified_ctx.get('applicable_laws', []), ensure_ascii=False)}
Language: {'Hindi' if is_hi else 'English'}
"""

    if gemini_key:
        try:
            ans = query_gemini_api(gemini_key, system_prompt, user_prompt)
            if ans and len(ans.strip()) > 10:
                return ans.strip()
        except Exception:
            pass

    if openai_key:
        try:
            ans = query_openai_api(openai_key, system_prompt, user_prompt)
            if ans and len(ans.strip()) > 10:
                return ans.strip()
        except Exception:
            pass

    # Intelligent deterministic offline fallback for common citizen follow-ups
    q_lower = follow_up_question.lower()
    if any(k in q_lower for k in ["police", "refuse", "fir", "मना", "थाना", "पुलिस"]):
        if is_hi:
            return (
                "यदि पुलिस थाना आपकी प्राथमिकी (FIR) दर्ज करने से मना करता है:\n"
                "1. भारतीय नागरिक सुरक्षा संहिता (BNSS), 2023 की धारा 173(4) के तहत आप अपनी लिखित शिकायत पंजीकृत डाक (Speed Post) द्वारा सीधे जिले के पुलिस अधीक्षक (SP / DCP) को भेज सकते हैं।\n"
                "2. आप संबंधित राज्य पुलिस के ऑनलाइन नागरिक पोर्टल या राष्ट्रीय साइबर पोर्टल (cybercrime.gov.in) पर ऑनलाइन ई-एफआईआर/शिकायत दर्ज कर सकते हैं।\n"
                "3. इसके बाद भी कार्रवाई न होने पर, BNSS की धारा 175(3) के अंतर्गत न्यायिक मजिस्ट्रेट की अदालत में अधिवक्ता या नालसा (15100) के मुफ्त वकील के माध्यम से प्रार्थना पत्र दिया जा सकता है।"
            )
        else:
            return (
                "If the police station refuses to register your FIR / complaint:\n"
                "1. Under Section 173(4) of the Bharatiya Nagarik Suraksha Sanhita (BNSS), 2023, you can send the substance of the information in writing by registered post to the Superintendent of Police (SP / DCP).\n"
                "2. You can submit an online complaint directly via your State Police Citizen Portal or the National Cyber Portal (cybercrime.gov.in).\n"
                "3. If inaction persists, you may approach the Judicial Magistrate under Section 175(3) of BNSS 2023 with assistance from District Legal Services Authority (DLSA / Helpline 15100)."
            )
    elif any(k in q_lower for k in ["fee", "cost", "charge", "खर्च", "फीस", "शुल्क"]):
        if is_hi:
            return (
                "कानूनी कार्यवाही व शिकायत हेतु शुल्क संबंधी जानकारी:\n"
                "1. साइबर हेल्पलाइन 1930 और राष्ट्रीय साइबर पोर्टल (cybercrime.gov.in) पर शिकायत दर्ज करना 100% निःशुल्क है।\n"
                "2. उपभोक्ता संरक्षण अधिनियम (CPA 2019) के तहत ₹5 लाख तक के दावों के लिए ई-दाखिल पोर्टल पर कोई कोर्ट फीस नहीं लगती।\n"
                "3. आरटीआई (RTI) आवेदन का वैधानिक शुल्क केवल ₹10 है (बीपीएल कार्ड धारकों के लिए पूर्णतः निःशुल्क)।\n"
                "4. नालसा (15100) और टेली-लॉ (14488) महिलाओं और पात्र नागरिकों को पूर्णतः निःशुल्क कानूनी सहायता प्रदान करते हैं।"
            )
        else:
            return (
                "Statutory fee and cost details:\n"
                "1. Filing on the National Cyber Crime Reporting Portal (1930 / cybercrime.gov.in) is 100% free.\n"
                "2. Under the Consumer Protection Act, 2019, claims up to ₹5,00,000 before the District Commission carry zero court fee.\n"
                "3. RTI applications require a nominal statutory fee of only ₹10 (exempt for Below Poverty Line applicants).\n"
                "4. Free legal aid and panel lawyers are available at zero cost via NALSA (15100) for eligible citizens under Section 12 of the LSA Act."
            )
    else:
        if is_hi:
            return (
                f"आपके प्रश्न '{follow_up_question}' के संदर्भ में प्रक्रियात्मक सलाह:\n"
                "1. अपने पास मौजूद सभी साक्ष्य (बैंक स्टेटमेंट, रसीदें, स्क्रीनशॉट, लिखित नोटिस) की 2-2 प्रमाणित प्रतियां तैयार रखें।\n"
                "2. संबंधित आधिकारिक पोर्टल या हेल्पलाइन पर अपनी शिकायत संदर्भ संख्या (Grievance Ref No.) दर्ज कराकर पावती सुरक्षित रखें।\n"
                "3. किसी भी प्रकार के संशय अथवा जटिल कानूनी स्थिति में नालसा हेल्पलाइन 15100 या टेली-लॉ (14488) पर निःशुल्क विधिक परामर्श प्राप्त करें।"
            )
        else:
            return (
                f"Procedural guidance for '{follow_up_question}':\n"
                "1. Keep duplicate certified copies of all primary evidence (bank transactions, receipts, chat records, notices).\n"
                "2. Quote your formal acknowledgment reference number in all subsequent correspondence with authorities.\n"
                "3. For tailored procedural assistance, contact the National Legal Services Authority (Helpline: 15100) or Tele-Law (14488)."
            )

