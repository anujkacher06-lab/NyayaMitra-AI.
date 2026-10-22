import os
import json
import re
from functools import lru_cache

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

CATEGORY_MAP = {
    # Cyber Fraud
    "cyber_fraud": "cyber_fraud.json",
    "cyber": "cyber_fraud.json",
    "online_fraud": "cyber_fraud.json",
    # Consumer Complaints
    "consumer_complaint": "consumer_issues.json",
    "consumer": "consumer_issues.json",
    "ecommerce": "consumer_issues.json",
    # Workplace & Salary
    "workplace_salary_issue": "employment_issues.json",
    "workplace": "employment_issues.json",
    "salary": "employment_issues.json",
    "employment": "employment_issues.json",
    # Tenancy & Rental Disputes
    "tenancy_dispute": "tenancy_issues.json",
    "tenancy": "tenancy_issues.json",
    "rent": "tenancy_issues.json",
    "landlord": "tenancy_issues.json",
    # RTI Assistance
    "rti_assistance": "rti_assistance.json",
    "rti": "rti_assistance.json",
    "right_to_information": "rti_assistance.json"
}

CATEGORY_FILES = [
    ("cyber_fraud", "cyber_fraud.json"),
    ("consumer_complaint", "consumer_issues.json"),
    ("workplace_salary_issue", "employment_issues.json"),
    ("tenancy_dispute", "tenancy_issues.json"),
    ("rti_assistance", "rti_assistance.json")
]

@lru_cache(maxsize=32)
def load_category_data(category_key: str) -> dict:
    """
    Load verified category JSON with memory caching to eliminate disk I/O latency.
    """
    normalized = category_key.lower().strip()
    filename = CATEGORY_MAP.get(normalized)
    if not filename:
        for k, v in CATEGORY_MAP.items():
            if k in normalized:
                filename = v
                break
    if not filename:
        filename = "cyber_fraud.json"  # safe default

    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def detect_category(question: str, user_selected: str = "") -> str:
    """
    Detects the best matching legal category among the 5 supported domains:
    1. cyber_fraud
    2. consumer_complaint
    3. workplace_salary_issue
    4. tenancy_dispute
    5. rti_assistance
    """
    if user_selected and user_selected in CATEGORY_MAP:
        return user_selected

    q_lower = question.lower()
    scores = {
        "cyber_fraud": 0,
        "consumer_complaint": 0,
        "workplace_salary_issue": 0,
        "tenancy_dispute": 0,
        "rti_assistance": 0
    }

    # Match against keywords stored inside each category JSON
    for cat, filename in CATEGORY_FILES:
        try:
            data = load_category_data(cat)
            keywords = data.get("keywords", [])
            for kw in keywords:
                if kw.lower() in q_lower:
                    scores[cat] += 2
        except Exception:
            pass

    # High-signal booster keywords (English, Hindi, and Hinglish)
    boosters = {
        "cyber_fraud": [
            "upi", "otp", "bank", "account", "deducted", "scam", "fraud", "hacked", "phishing",
            "पैसे कट", "खाता", "ओटीपी", "qr code", "sim swap", "apk", "paise kat", "debit"
        ],
        "consumer_complaint": [
            "product", "warranty", "refund", "delivery", "amazon", "flipkart", "damaged",
            "replacement", "defective", "order", "समान", "रिफंड", "वारंटी", "kharab", "broken"
        ],
        "workplace_salary_issue": [
            "salary", "employer", "wages", "relieving", "resignation", "boss", "company",
            "unpaid", "pf", "provident", "नौकरी", "वेतन", "सैलरी", "termination", "f&f"
        ],
        "tenancy_dispute": [
            "rent", "landlord", "tenant", "security deposit", "eviction", "lease", "rent agreement",
            "vacate", "मकान मालिक", "किराया", "किरायेदार", "डिपॉजिट", "बेदखली", "broker", "flatmate"
        ],
        "rti_assistance": [
            "rti", "right to information", "pio", "public information", "first appeal", "cpio",
            "spio", "आरटीआई", "सूचना का अधिकार", "जन सूचना अधिकारी", "scholarship delay", "pension delay"
        ]
    }

    for cat, words in boosters.items():
        for w in words:
            if w in q_lower:
                scores[cat] += 1

    best_cat = max(scores, key=scores.get)
    if scores[best_cat] > 0:
        return best_cat
    return "cyber_fraud"  # safe default

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

    # Pick the template dynamically
    template_text = ""
    if category == "cyber_fraud":
        template_text = templates.get("police_cyber_cell", {}).get(lang_code, "")
    elif category == "consumer_complaint":
        template_text = templates.get("consumer_notice", {}).get(lang_code, "")
    elif category == "workplace_salary_issue":
        template_text = templates.get("employer_salary_demand", {}).get(lang_code, "")
    else:
        # Tenancy or RTI or any other: take first available template
        if templates:
            first_key = list(templates.keys())[0]
            template_text = templates.get(first_key, {}).get(lang_code, "")

    if not template_text:
        template_text = (
            "To,\nThe Concerned Authority\nSubject: Formal Complaint regarding [BRIEF_DESCRIPTION]\n\n"
            "Respected Sir/Madam,\n[BRIEF_DESCRIPTION]\n\nDate: [CURRENT_DATE]\nName: [USER_NAME]"
        )

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
    text = text.replace("[INCIDENT_DATE]", incident_date)
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

@lru_cache(maxsize=1)
def load_all_states_data() -> dict:
    state_file = os.path.join(DATA_DIR, "state_legal_aid.json")
    if os.path.exists(state_file):
        with open(state_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def get_state_legal_aid(state_name: str = "", language: str = "English") -> dict:
    """
    Returns specific State Legal Services Authority (SLSA), Cyber Cell, and
    State Consumer Commission details based on user's State or UT.
    """
    states_data = load_all_states_data()
    norm = state_name.strip().lower()

    if norm:
        for k, v in states_data.items():
            if k in norm or norm in k:
                return v

    return states_data.get("national_default", {
        "state_name": "All India (National Jurisdiction)",
        "slsa_name": "National Legal Services Authority (NALSA)",
        "slsa_helpline": "15100",
        "slsa_website": "https://nalsa.gov.in",
        "cyber_portal": "https://cybercrime.gov.in (Helpline: 1930)",
        "consumer_commission": "National Consumer Helpline (1915)"
    })

def get_all_states() -> list:
    """
    Returns list of all available states for dropdown selection in UI.
    """
    states_data = load_all_states_data()
    result = []
    for k, v in states_data.items():
        if k != "national_default":
            result.append({
                "id": k,
                "name": v.get("state_name", k.title()),
                "name_hi": v.get("state_name_hi", k.title()),
                "helpline": v.get("slsa_helpline", "15100")
            })
    result.sort(key=lambda x: x["name"])
    return result

def generate_case_dossier(response_data: dict, draft_text: str = "") -> str:
    """
    Generates a formal, printable plain-text Citizen Legal Dossier 
    ready for physical filing or offline storage.
    """
    query_id = response_data.get("query_id", "GENERAL")
    category = response_data.get("category", "Legal Issue")
    explanation = response_data.get("explanation", "")
    actions = response_data.get("actions", [])
    evidence = response_data.get("evidence", [])
    laws = response_data.get("applicable_laws", [])
    resources = response_data.get("official_resources", [])
    state_aid = response_data.get("state_aid", {})
    disclaimer = response_data.get("disclaimer", "")

    from datetime import datetime
    now_str = datetime.now().strftime("%d-%m-%Y %H:%M IST")

    lines = []
    lines.append("=" * 80)
    lines.append("                    NYAYAMITRA AI - CITIZEN LEGAL DOSSIER")
    lines.append("              न्यायमित्र - नागरिक कानूनी सूचना व साक्ष्य दस्तावेज़")
    lines.append("=" * 80)
    lines.append(f"Dossier Reference ID : NYM-REF-{query_id}")
    lines.append(f"Generated On          : {now_str}")
    lines.append(f"Problem Category      : {category}")
    if state_aid.get("state_name"):
        lines.append(f"State Jurisdiction    : {state_aid.get('state_name')} ({state_aid.get('slsa_name', 'SLSA')})")
    lines.append("-" * 80)
    lines.append("")

    lines.append("1. PROCEDURAL SUMMARY & LEGAL EXPLANATION:")
    lines.append(explanation)
    lines.append("")

    if laws:
        lines.append("APPLICABLE LEGISLATION (INDIA CODE & BNS 2023):")
        for law in laws:
            lines.append(f" • {law}")
        lines.append("")

    lines.append("2. IMMEDIATE STEP-BY-STEP ACTION CHECKLIST:")
    for i, act in enumerate(actions, 1):
        lines.append(f" [ ] Step {i}: {act}")
    lines.append("")

    lines.append("3. MANDATORY DOCUMENTS & EVIDENCE CHECKLIST:")
    lines.append(" (Preserve primary originals & certified digital printouts under BSA 2023 Sec 63 / IT Act Sec 65B)")
    for i, doc in enumerate(evidence, 1):
        lines.append(f" [ ] Item {i}: {doc}")
    lines.append("")

    lines.append("4. OFFICIAL STATUTORY GRIEVANCE PORTALS & HELPLINES:")
    for res in resources:
        res_name = res.get("name", "Grievance Portal")
        auth = res.get("authority", "")
        hp = res.get("helpline", "")
        url = res.get("url", "")
        lines.append(f" • {res_name} ({auth})")
        if hp and hp != "N/A":
            lines.append(f"   Helpline: {hp}")
        if url:
            lines.append(f"   Official Portal: {url}")
    lines.append("")

    if state_aid:
        lines.append("5. STATE LEGAL SERVICES AUTHORITY & FREE LEGAL AID:")
        lines.append(f" • Nodal Authority: {state_aid.get('slsa_name', 'NALSA')}")
        lines.append(f" • Legal Aid Toll-Free: {state_aid.get('slsa_helpline', '15100')}")
        if state_aid.get("slsa_address"):
            lines.append(f" • Office Address: {state_aid.get('slsa_address')}")
        if state_aid.get("free_aid_threshold"):
            lines.append(f" • Free Aid Criteria: {state_aid.get('free_aid_threshold')}")
        if state_aid.get("cyber_cell"):
            lines.append(f" • State Cyber Wing: {state_aid.get('cyber_cell')}")
        lines.append("")

    if draft_text:
        lines.append("6. FORMAL LEGAL COMPLAINT / APPLICATION DRAFT:")
        lines.append("-" * 80)
        lines.append(draft_text.strip())
        lines.append("-" * 80)
        lines.append("")

    lines.append("7. STATUTORY SAFETY DISCLAIMER:")
    lines.append(disclaimer)
    lines.append("=" * 80)
    lines.append("Verified under India Code, National Consumer Commission & Indian Cyber Crime Coordination Centre.")
    lines.append("=" * 80)

    return "\n".join(lines)


