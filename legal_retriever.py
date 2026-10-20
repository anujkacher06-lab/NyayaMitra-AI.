import os
import json
import re

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

CATEGORY_MAP = {
    "cyber_fraud": "cyber_fraud.json",
    "cyber": "cyber_fraud.json",
    "consumer_complaint": "consumer_issues.json",
    "consumer": "consumer_issues.json",
    "workplace_salary_issue": "employment_issues.json",
    "workplace": "employment_issues.json",
    "salary": "employment_issues.json"
}

def load_category_data(category_key: str):
    normalized = category_key.lower().strip()
    filename = CATEGORY_MAP.get(normalized)
    if not filename:
        for k, v in CATEGORY_MAP.items():
            if k in normalized:
                filename = v
                break
    if not filename:
        filename = "cyber_fraud.json" # default fallback
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def detect_category(question: str, user_selected: str = "") -> str:
    """
    If user selected a specific category, respect it unless it's empty or 'auto'.
    Otherwise, match against keywords in all 3 knowledge bases.
    """
    if user_selected and user_selected in CATEGORY_MAP:
        return user_selected

    q_lower = question.lower()
    scores = {"cyber_fraud": 0, "consumer_complaint": 0, "workplace_salary_issue": 0}

    for cat, filename in [("cyber_fraud", "cyber_fraud.json"),
                          ("consumer_complaint", "consumer_issues.json"),
                          ("workplace_salary_issue", "employment_issues.json")]:
        path = os.path.join(DATA_DIR, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            keywords = data.get("keywords", [])
            for kw in keywords:
                if kw.lower() in q_lower:
                    scores[cat] += 2
                    
    # Keyword boosters for common phrases
    cyber_words = ["upi", "otp", "bank", "account", "deducted", "scam", "fraud", "hacked", "phishing", "पैसे कट", "खाता", "ओटीपी"]
    consumer_words = ["product", "warranty", "refund", "delivery", "amazon", "flipkart", "damaged", "replacement", "defective", "order", "समान", "रिफंड"]
    salary_words = ["salary", "employer", "wages", "relieving", "resignation", "boss", "company", "unpaid", "pf", "provident", "नौकरी", "वेतन", "सैलरी"]

    for w in cyber_words:
        if w in q_lower: scores["cyber_fraud"] += 1
    for w in consumer_words:
        if w in q_lower: scores["consumer_complaint"] += 1
    for w in salary_words:
        if w in q_lower: scores["workplace_salary_issue"] += 1

    best_cat = max(scores, key=scores.get)
    if scores[best_cat] > 0:
        return best_cat
    return "cyber_fraud" # safe default

def get_verified_context(category: str, language: str = "English") -> dict:
    lang_code = "hi" if language.lower().startswith("hi") else "en"
    raw = load_category_data(category)
    
    title = raw.get("title", {}).get(lang_code, raw.get("title", {}).get("en", category))
    explanation = raw.get("simple_explanation", {}).get(lang_code, raw.get("simple_explanation", {}).get("en", ""))
    actions = raw.get("immediate_actions", {}).get(lang_code, raw.get("immediate_actions", {}).get("en", []))
    evidence = raw.get("evidence_checklist", {}).get(lang_code, raw.get("evidence_checklist", {}).get("en", []))
    laws = raw.get("applicable_laws", [])
    resources = raw.get("official_resources", [])
    verified_date = raw.get("verified_date", "2026-07-16")
    templates = raw.get("complaint_template", {})

    return {
        "category_id": category,
        "title": title,
        "explanation": explanation,
        "actions": actions,
        "evidence": evidence,
        "applicable_laws": laws,
        "resources": resources,
        "verified_date": verified_date,
        "templates": templates,
        "lang_code": lang_code
    }

def generate_local_complaint_draft(category: str, language: str = "English", user_details: dict = None) -> str:
    lang_code = "hi" if language.lower().startswith("hi") else "en"
    ctx = get_verified_context(category, language)
    templates = ctx.get("templates", {})
    
    if user_details is None:
        user_details = {}

    from datetime import datetime
    today_str = datetime.now().strftime("%d-%m-%Y")

    # Pick the template
    template_text = ""
    if category == "cyber_fraud":
        template_text = templates.get("police_cyber_cell", {}).get(lang_code, "")
    elif category == "consumer_complaint":
        template_text = templates.get("consumer_notice", {}).get(lang_code, "")
    elif category == "workplace_salary_issue":
        template_text = templates.get("employer_salary_demand", {}).get(lang_code, "")

    if not template_text:
        template_text = "To,\nThe Concerned Authority\nSubject: Formal Complaint regarding [ISSUE]\n\nRespected Sir/Madam,\n[DETAILS]\n\nDate: [CURRENT_DATE]\nName: [USER_NAME]"

    # Replacement values
    name = user_details.get("name") or ("[Your Full Name / आपका नाम]" if lang_code == "en" else "[आपका पूरा नाम]")
    address = user_details.get("address") or ("[Your Residential Address, City, PIN]" if lang_code == "en" else "[आपका आवासीय पता, शहर, पिनकोड]")
    phone = user_details.get("phone") or ("[Your 10-digit Mobile Number]" if lang_code == "en" else "[आपका 10 अंकों का मोबाइल नंबर]")
    email = user_details.get("email") or ("[your.email@example.com]" if lang_code == "en" else "[आपका ईमेल आईडी]")
    amount = user_details.get("amount") or ("[Amount in ₹ / राशि]")
    incident_date = user_details.get("incident_date") or ("[Date of Incident / घटना की तारीख]")
    time_val = user_details.get("time") or ("[Time / समय]")
    desc = user_details.get("description") or ("[Specific factual summary of what happened / घटना का संक्षिप्त विवरण]")

    text = template_text
    text = text.replace("[USER_NAME]", name)
    text = text.replace("[USER_ADDRESS]", address)
    text = text.replace("[USER_PHONE]", phone)
    text = text.replace("[USER_EMAIL]", email)
    text = text.replace("[AMOUNT]", amount)
    text = text.replace("[TOTAL_AMOUNT]", amount)
    text = text.replace("[CURRENT_DATE]", today_str)
    text = text.replace("[DATE]", incident_date)
    text = text.replace("[TIME]", time_val)
    text = text.replace("[BRIEF_DESCRIPTION]", desc)
    text = text.replace("[BRIEF_DESCRIPTION_OF_DEFECT]", desc)

    disclaimer_header = (
        "/* =========================================================================\n"
        "   DISCLAIMER: This is an editable draft legal template provided for\n"
        "   informational purposes by NyayaMitra AI. Review, verify all factual\n"
        "   details, and consult legal aid (NALSA/Tele-Law) before formal submission.\n"
        "   ========================================================================= */\n\n"
        if lang_code == "en" else
        "/* =========================================================================\n"
        "   अस्वीकरण: यह NyayaMitra AI द्वारा सूचनात्मक उद्देश्यों हेतु तैयार किया गया\n"
        "   एक संपादन योग्य शिकायत प्रारूप है। कृपया जमा करने से पहले सभी तथ्यों की जांच\n"
        "   करें एवं कानूनी सहायता (नालसा/टेली-लॉ) से सलाह लें।\n"
        "   ========================================================================= */\n\n"
    )

    return disclaimer_header + text
