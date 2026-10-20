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
