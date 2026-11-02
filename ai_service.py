import os
import json
import requests
import io
import re
import base64
from PIL import Image
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

    if lang_code == "hi":
        help_needed = (
            "यदि मामला ₹5,00,000 से अधिक की धोखाधड़ी का हो, या नियोक्ता/कंपनी द्वारा निरंतर उत्पीड़न "
            "अथवा धमकी दी जा रही हो, तो नालसा (NALSA) के निःशुल्क विधिक सेवा वकील या टेली-लॉ (Tele-Law) से तत्काल संपर्क करें।"
        )
        disclaimer = (
            "महत्वपूर्ण अस्वीकरण: यह केवल सामान्य कानूनी जानकारी और प्रक्रियात्मक मार्गदर्शन है, "
            "कोई पेशेवर कानूनी सलाह नहीं। किसी भी औपचारिक कानूनी कार्रवाई से पहले योग्य अधिवक्ता या विधिक सेवा प्राधिकरण से परामर्श करें।"
        )
    elif lang_code == "ta":
        help_needed = (
            "நிதி இழப்பு ₹5,00,000 க்கு மேல் இருந்தால் அல்லது சிக்கலான பல மாநில மோசடி, குற்றப் பயமுறுத்தல் இருந்தால், "
            "NALSA / டெலி-லா (Tele-Law) மூலம் இலவச சட்ட உதவி பெறுங்கள்."
        )
        disclaimer = (
            "முக்கியமான மறுப்பு: இது பொதுவான சட்டத் தகவல் மற்றும் செயல்முறை வழிகாட்டுதல் மட்டுமே, தொழில்முறை சட்ட ஆலோசனை அல்ல. "
            "NyayaMitra எந்த சட்ட முடிவையும் உத்தரவாதம் அளிக்காது. சான்றிதழ் பெற்ற சட்ட ஆலோசகர் அல்லது DLSA உடன் சரிபார்க்கவும்."
        )
    elif lang_code == "te":
        help_needed = (
            "ఆర్థిక నష్టం ₹5,00,000 మించినట్లయితే లేదా సంక్లిష్టమైన బహుళ-అధికార పరిధి మోసం, నేరపరమైన బెదిరింపు ఉన్నట్లయితే, "
            "NALSA / టెలీ-లా (Tele-Law) ద్వారా ఉచిత న్యాయ సహాయం పొందండి."
        )
        disclaimer = (
            "ముఖ్యమైన నిరాకరణ: ఇది సాధారణ చట్టపరమైన సమాచారం మాత్రమే, వృత్తిపరమైన న్యాయ సలహా కాదు. "
            "NyayaMitra ఏ న్యాయపరమైన ఫలితాన్నీ హామీ ఇవ్వదు. ధృవీకరించిన న్యాయ నిపుణుడు లేదా DLSA తో నిర్ధారించుకోండి."
        )
    elif lang_code == "bn":
        help_needed = (
            "আর্থিক ক্ষতি ₹5,00,000 ছাড়িয়ে গেলে বা জটিল বহু-এখতিয়ার প্রতারণা, অপরাধমূলক ভয় দেখানো হলে, "
            "NALSA / টেলি-ল (Tele-Law) এর মাধ্যমে বিনামূল্যে আইনি সহায়তা নিন।"
        )
        disclaimer = (
            "গুরুত্বপূর্ণ দাবিত্যাগ: এটি শুধুমাত্র সাধারণ আইনি তথ্য এবং পদ্ধতিগত নির্দেশিকা, পেশাদার আইনি পরামর্শ নয়। "
            "NyayaMitra কোনো আইনি ফলাফলের গ্যারান্টি দেয় না। সার্টিফাইড আইনজীবী বা DLSA এর সাথে যোগাযোগ করুন।"
        )
    elif lang_code == "mr":
        help_needed = (
            "आर्थिक नुकसान ₹5,00,000 पेक्षा जास्त असल्यास किंवा गुंतागुंतीची बहु-क्षेत्राधिकार फसवणूक, गुन्हेगारी धमकी असल्यास, "
            "NALSA / टेली-लॉ (Tele-Law) द्वारे मोफत कायदेशीर मदत मिळवा."
        )
        disclaimer = (
            "महत्त्वाचा अस्वीकरण: ही केवळ सामान्य कायदेशीर माहिती व प्रक्रियात्मक मार्गदर्शन आहे, व्यावसायिक कायदेशीर सल्ला नाही. "
            "NyayaMitra कोणत्याही कायदेशीर परिणामाची हमी देत नाही. प्रमाणित वकील किंवा DLSA कडे तपासणी करा."
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
    # Use Gemini REST API with header-based authentication to avoid logging API keys in URLs
    candidate_models = ["gemini-3.5-flash", "gemini-flash-latest", "gemini-2.5-flash", "gemini-1.5-flash"]
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
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }
    last_err = None
    for model in candidate_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=22)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    return candidates[0]["content"]["parts"][0]["text"]
            last_err = f"Status {resp.status_code}: {resp.text[:150]}"
        except Exception as e:
            last_err = str(e)
            continue
    raise Exception(f"Gemini API returned error: {last_err}")

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

    # Add explicit language instruction for non-English/Hindi languages so AI responds fully in that language
    lang_instruction = ""
    if lang_code not in ("en", "hi") and language.lower() not in ("english", "hindi"):
        lang_instruction = f"\n\nIMPORTANT: Respond ENTIRELY in {language}. Do not mix any other language in your response."

    user_content = f"""
USER QUESTION:
"{question}"

PREFERRED LANGUAGE: {language}{lang_instruction}

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

    # For non-English/Hindi languages, instruct AI to respond in that language
    lang_note = f" Respond ENTIRELY in {language}." if not is_hi and not language.lower().startswith("en") else ""

    system_prompt = (
        "You are NyayaMitra AI, an Indian legal information assistant. "
        "Answer the citizen's follow-up question concisely (max 3-4 bullet points), grounded in Indian law (BNS 2023, BNSS 2023, CPA 2019, RTI 2005). "
        f"Never invent laws or citation numbers. Always advise consulting DLSA/NALSA (15100) or Tele-Law (14488) for professional counsel.{lang_note}"
        if not is_hi else
        "आप न्यायमित्र (NyayaMitra AI) हैं। नागरिक के अनुवर्ती (follow-up) प्रश्न का संक्षिप्त और स्पष्ट उत्तर 3-4 बिंदुओं में दें। "
        "उत्तर भारतीय कानून (BNS 2023, BNSS 2023, CPA 2019, RTI 2005) पर आधारित होना चाहिए। "
        "नालसा (15100) या टेली-लॉ (14488) से विधिक परामर्श लेने का सुझाव दें।"
    )

    user_prompt = f"""Case Category: {category}
Original Citizen Problem: {original_question}
Follow-up Question: {follow_up_question}
Verified Statutes: {json.dumps(verified_ctx.get('applicable_laws', []), ensure_ascii=False)}
Language: {language}
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

VISION_OCR_PROMPT = """You are an expert Indian legal aid OCR and transaction receipt parser for NyayaMitra AI.
Analyze this document image (which may be a UPI payment receipt, bank debit SMS screenshot, e-commerce order invoice, rent agreement notice, or workplace salary slip).
Carefully transcribe all readable text and extract key legal and transaction entities.

Return ONLY a valid JSON object matching this schema:
{
  "extracted_text": "Complete transcribed text from the image, preserving numbers, names, and timestamps accurately.",
  "amount": "The transaction or claim amount with comma formatting if present (e.g. '14,500' or '5,000.00'), or empty string if not found",
  "utr": "The 12-digit UPI UTR reference number or bank transaction ID, or empty string if not found",
  "incident_date": "The date of the transaction or notice in DD/MM/YYYY or readable date format, or empty string if not found",
  "payment_app": "The app or channel if identifiable (e.g. 'PhonePe', 'Google Pay', 'Paytm', 'BHIM', 'SBI YONO', 'Netbanking'), or empty string",
  "sender_or_victim": "Name of sender/remitter/complainant if visible, or empty string",
  "recipient_or_accused": "Name of recipient/merchant/landlord/accused if visible, or empty string",
  "detected_category": "One of: 'cyber_fraud', 'consumer_complaint', 'workplace_salary_issue', 'tenancy_dispute', 'rti_assistance'",
  "summary": "A concise 1-2 sentence factual summary of the incident for a formal legal complaint (e.g. 'Unauthorized UPI debit of ₹14,500 via PhonePe on 15/07/2026 with UTR 412345678901.')"
}
"""

def query_gemini_vision(api_key: str, image_bytes: bytes, mime_type: str, prompt: str = VISION_OCR_PROMPT) -> dict:
    """
    Multimodal Gemini Vision OCR for receipts and legal documents.
    """
    candidate_models = ["gemini-3.5-flash", "gemini-flash-latest", "gemini-2.5-flash", "gemini-1.5-flash"]
    b64_img = base64.b64encode(image_bytes).decode("utf-8")
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": mime_type or "image/jpeg",
                            "data": b64_img
                        }
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "responseMimeType": "application/json"
        }
    }
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }
    last_err = None
    for model in candidate_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=22)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    raw_text = candidates[0]["content"]["parts"][0]["text"]
                    return json.loads(raw_text)
            last_err = f"Status {resp.status_code}: {resp.text[:150]}"
        except Exception as e:
            last_err = str(e)
            continue
    raise Exception(f"Gemini Vision API returned error: {last_err}")

def query_openai_vision(api_key: str, image_bytes: bytes, mime_type: str, prompt: str = VISION_OCR_PROMPT) -> dict:
    """
    Multimodal OpenAI GPT-4o-mini Vision OCR for receipts and legal documents.
    """
    url = "https://api.openai.com/v1/chat/completions"
    b64_img = base64.b64encode(image_bytes).decode("utf-8")
    mime = mime_type or "image/jpeg"
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime};base64,{b64_img}"
                        }
                    }
                ]
            }
        ],
        "response_format": {"type": "json_object"}
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=15)
    if resp.status_code == 200:
        data = resp.json()
        raw_text = data["choices"][0]["message"]["content"]
        return json.loads(raw_text)
    raise Exception(f"OpenAI Vision API returned status {resp.status_code}")

def extract_entities_from_text(text: str) -> dict:
    """
    Regex entity extraction tailored for Indian payment apps, UPI, and civil legal disputes.
    """
    # Amount
    amt_match = re.search(r'(?:₹|rs\.?|inr)\s*([0-9,]+(?:\.\d{2})?)', text, re.IGNORECASE)
    if not amt_match:
        amt_match = re.search(r'(?:debited|deducted|paid|amount|amt)[:\s]*([0-9,]+(?:\.\d{2})?)', text, re.IGNORECASE)
    amount = amt_match.group(1).strip() if amt_match else ""

    # UTR / 12-digit transaction reference
    utr_match = re.search(r'\b(?:utr|ref|rrn|upi\s*ref|txn\s*id)?[:\s#]*([0-9]{12})\b', text, re.IGNORECASE)
    if not utr_match:
        utr_match = re.search(r'\b([0-9]{12})\b', text)
    utr = utr_match.group(1).strip() if utr_match else ""

    # Incident Date
    date_match = re.search(r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b', text)
    if not date_match:
        date_match = re.search(r'\b(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4})\b', text, re.IGNORECASE)
    incident_date = date_match.group(1).strip() if date_match else ""

    # Payment App / Channel
    app_match = re.search(r'\b(PhonePe|Google\s*Pay|GPay|Paytm|BHIM|Cred|Amazon\s*Pay|SBI\s*YONO|HDFC|ICICI|Axis|Kotak)\b', text, re.IGNORECASE)
    payment_app = app_match.group(1).strip() if app_match else ""

    import legal_retriever
    detected_cat = legal_retriever.detect_category(text)

    return {
        "amount": amount,
        "utr": utr,
        "incident_date": incident_date,
        "payment_app": payment_app,
        "sender_or_victim": "",
        "recipient_or_accused": "",
        "detected_category": detected_cat,
        "summary": ""
    }

def build_auto_fill_prompt(entities: dict, extracted_text: str = "", language: str = "English") -> str:
    is_hi = language.lower().startswith("hi")
    summary = entities.get("summary", "").strip()
    if summary:
        return summary

    amount = entities.get("amount", "").strip()
    utr = entities.get("utr", "").strip()
    date_val = entities.get("incident_date", "").strip()
    app_val = entities.get("payment_app", "").strip()
    cat = entities.get("detected_category", "cyber_fraud")

    parts = []
    if is_hi:
        if amount:
            parts.append(f"₹{amount} की राशि")
        if app_val:
            parts.append(f"{app_val} के माध्यम से")
        if utr:
            parts.append(f"यूटीआर {utr} के साथ")
        if date_val:
            parts.append(f"दिनांक {date_val} को")

        if cat == "cyber_fraud":
            return (" ".join(parts) + " अनाधिकृत रूप से कट गई है। कृपया तुरंत कानूनी प्रक्रिया एवं 1930 हेल्पलाइन पर शिकायत दर्ज करने का मार्गदर्शन दें।").strip()
        elif cat == "consumer_complaint":
            return (" ".join(parts) + " का भुगतान करने पर भी खराब सामान मिला और रिफंड नहीं दिया गया। उपभोक्ता फोरम में शिकायत हेतु मार्गदर्शन दें।").strip()
        elif cat == "workplace_salary_issue":
            return (" ".join(parts) + " का बकाया वेतन कंपनी द्वारा नहीं दिया गया है। लेबर कमिश्नर के समक्ष शिकायत हेतु सहायता चाहिए।").strip()
        elif cat == "tenancy_dispute":
            return (" ".join(parts) + " का सिक्योरिटी डिपॉजिट मकान मालिक वापस नहीं कर रहा है। रेंट अथॉरिटी के पास शिकायत दर्ज करनी है।").strip()
        else:
            return (" ".join(parts) + " से संबंधित मामले में सूचना का अधिकार (RTI) के तहत जानकारी चाहिए।").strip()
    else:
        if amount:
            parts.append(f"₹{amount}")
        if app_val:
            parts.append(f"via {app_val}")
        if utr:
            parts.append(f"with UTR Ref: {utr}")
        if date_val:
            parts.append(f"on {date_val}")

        if cat == "cyber_fraud":
            return ("Unauthorized deduction of " + " ".join(parts) + ". Money was debited without my consent after receiving a link. Please guide on filing under 1930 and BNS 2023.").strip()
        elif cat == "consumer_complaint":
            return ("Paid " + " ".join(parts) + " for a product/service, but received defective goods and merchant refused refund. Need guidance for e-Daakhil / NCH.").strip()
        elif cat == "workplace_salary_issue":
            return ("Pending salary/dues of " + " ".join(parts) + " withheld by employer. Need procedure for Samadhan portal and Labour Commissioner.").strip()
        elif cat == "tenancy_dispute":
            return ("Security deposit of " + " ".join(parts) + " illegally withheld by landlord after vacating. Need guidance under Model Tenancy Act.").strip()
        else:
            return ("Seeking official records regarding payment of " + " ".join(parts) + " under RTI Act 2005.").strip()

def parse_document_or_receipt(file_bytes: bytes = b"", filename: str = "", mime_type: str = "", text_context: str = "", language: str = "English") -> dict:
    """
    Unified multi-tiered OCR & receipt parser for NyayaMitra AI:
    - Tier 1: Cloud Vision OCR via Gemini 1.5 Flash (highest accuracy for UPI apps/receipts)
    - Tier 2: Cloud Vision OCR via OpenAI GPT-4o-mini
    - Tier 3: Local Pytesseract OCR (if installed)
    - Tier 4: Text stream & Pillow image metadata fallback with intelligent guidance
    """
    raw_text = (text_context or "").strip()
    note = ""
    ocr_engine = "Text Entity Parser"
    entities = {}

    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("AI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    ext = os.path.splitext(filename)[1].lower() if filename else ""

    # Check if a text file was uploaded
    if file_bytes and ext in [".txt", ".csv", ".log", ".json"]:
        try:
            file_text = file_bytes.decode("utf-8", errors="ignore")
            raw_text = (raw_text + "\n" + file_text).strip()
            ocr_engine = "Plaintext Log Parser"
        except Exception:
            pass

    # Check if an image file was uploaded
    is_image = False
    img_format = ""
    img_size = ()
    if file_bytes and ext not in [".txt", ".csv", ".log", ".json"]:
        try:
            with Image.open(io.BytesIO(file_bytes)) as pil_img:
                img_format = pil_img.format or "Image"
                img_size = pil_img.size
                is_image = True
        except Exception:
            is_image = False

    if is_image:
        mime_map = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
            ".bmp": "image/bmp",
            ".gif": "image/gif"
        }
        effective_mime = mime_type if mime_type and "/" in mime_type else mime_map.get(ext, "image/jpeg")

        # Tier 1: Gemini Vision
        if gemini_key:
            try:
                vision_result = query_gemini_vision(gemini_key, file_bytes, effective_mime)
                if isinstance(vision_result, dict) and (vision_result.get("extracted_text") or vision_result.get("amount") or vision_result.get("utr")):
                    entities = {
                        "amount": str(vision_result.get("amount", "") or ""),
                        "utr": str(vision_result.get("utr", "") or ""),
                        "incident_date": str(vision_result.get("incident_date", "") or ""),
                        "payment_app": str(vision_result.get("payment_app", "") or ""),
                        "sender_or_victim": str(vision_result.get("sender_or_victim", "") or ""),
                        "recipient_or_accused": str(vision_result.get("recipient_or_accused", "") or ""),
                        "detected_category": str(vision_result.get("detected_category", "cyber_fraud")),
                        "summary": str(vision_result.get("summary", "") or "")
                    }
                    raw_text = str(vision_result.get("extracted_text", "") or raw_text)
                    ocr_engine = "Gemini 1.5 Flash Vision"
            except Exception as e:
                print(f"Gemini Vision call failed, trying next tier: {e}")

        # Tier 2: OpenAI Vision
        if not entities and openai_key:
            try:
                vision_result = query_openai_vision(openai_key, file_bytes, effective_mime)
                if isinstance(vision_result, dict) and (vision_result.get("extracted_text") or vision_result.get("amount") or vision_result.get("utr")):
                    entities = {
                        "amount": str(vision_result.get("amount", "") or ""),
                        "utr": str(vision_result.get("utr", "") or ""),
                        "incident_date": str(vision_result.get("incident_date", "") or ""),
                        "payment_app": str(vision_result.get("payment_app", "") or ""),
                        "sender_or_victim": str(vision_result.get("sender_or_victim", "") or ""),
                        "recipient_or_accused": str(vision_result.get("recipient_or_accused", "") or ""),
                        "detected_category": str(vision_result.get("detected_category", "cyber_fraud")),
                        "summary": str(vision_result.get("summary", "") or "")
                    }
                    raw_text = str(vision_result.get("extracted_text", "") or raw_text)
                    ocr_engine = "GPT-4o Mini Vision"
            except Exception as e:
                print(f"OpenAI Vision call failed, trying next tier: {e}")

        # Tier 3: Local Pytesseract (if available)
        if not entities:
            try:
                import pytesseract
                with Image.open(io.BytesIO(file_bytes)) as pil_img:
                    tess_text = pytesseract.image_to_string(pil_img)
                    if tess_text.strip():
                        raw_text = tess_text.strip()
                        entities = extract_entities_from_text(raw_text)
                        ocr_engine = "Tesseract Local OCR"
            except Exception:
                pass

        # Tier 4: Image Metadata Fallback
        if not entities:
            combined = f"{filename} {raw_text}".strip()
            entities = extract_entities_from_text(combined)
            ocr_engine = "Pillow Image Inspector"
            note = (
                f"Uploaded image: {img_format} ({img_size[0]}x{img_size[1]}). "
                "Automated AI Vision OCR is active when GEMINI_API_KEY is configured in .env. "
                "You can also paste the transaction SMS or receipt text directly below."
            )
    elif file_bytes and not is_image:
        combined = f"{filename} {raw_text}".strip()
        entities = extract_entities_from_text(combined)
        note = (
            "Uploaded file received. For automated OCR entity extraction, "
            "upload a valid PNG/JPEG receipt image or paste transaction details."
        )
    else:
        # Pure text analysis
        entities = extract_entities_from_text(raw_text)

    # Ensure detected_category is always populated
    if not entities.get("detected_category"):
        import legal_retriever
        entities["detected_category"] = legal_retriever.detect_category(raw_text or filename)

    auto_prompt = build_auto_fill_prompt(entities, raw_text, language)

    payload = {
        "status": "success",
        "ocr_engine": ocr_engine,
        "extracted_text": raw_text[:800] if len(raw_text) > 800 else raw_text,
        "entities": entities,
        "auto_fill_prompt": auto_prompt
    }
    if note:
        payload["note"] = note
    return payload

