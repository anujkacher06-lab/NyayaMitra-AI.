# NyayaMitra AI (न्यायमित्र)
> **Simple, Safe and Accessible Legal Information for Every Indian**

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/framework-Flask%203.1-black.svg)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/database-SQLite-lightgrey.svg)](https://www.sqlite.org/)
[![Status](https://img.shields.io/badge/MVP-Verified%20under%20India%20Code-green.svg)](https://www.indiacode.nic.in/)

NyayaMitra AI is an Indian legal-information assistant designed to empower citizens by translating complex procedural laws into clear, empathetic, and actionable guidance. It recommends official government grievance resources, delivers interactive evidence checklists, and generates customizable formal complaint drafts in **English** and **Hindi**.

---

## 🎯 Expanded Civic Scope: 5 High-Impact Categories

To deliver grounded, hallucination-resistant legal information, NyayaMitra AI anchors its guidance directly in verified **India Code** statutes, updated criminal codes (**BNS 2023** and **BNSS 2023**), and official government portals:

1. **Cyber & Financial Fraud**
   - UPI scams, OTP fraud, phishing links, unauthorized bank debits, fake loan apps, impersonation.
   - Statutory provisions: **Information Technology Act, 2000** (Sec 66C, 66D); **Bharatiya Nyaya Sanhita (BNS), 2023** (Sec 318 - Cheating, Sec 319 - Cheating by personation).
   - Evidence preservation: Electronic record certification notes under **Section 63 of Bharatiya Sakshya Adhiniyam, 2023 (BSA)** / IT Act Sec 65B.
   - Emergency response: Immediate freeze within "Golden Hour" via **1930 Helpline** & [cybercrime.gov.in](https://cybercrime.gov.in).

2. **Consumer Complaints & Disputes**
   - Defective goods, delivery damages, refused refunds, false advertising, e-commerce service deficiency.
   - Statutory provisions: **Consumer Protection Act, 2019**; Consumer Protection (E-Commerce) Rules, 2020.
   - Government portals: **National Consumer Helpline (NCH 1915)**, **INGRAM**, and **e-Daakhil** online commission filing (zero court fee up to ₹5 Lakh claims).

3. **Workplace & Salary Issues**
   - Unpaid wages, delayed salaries, withheld relieving letters, illegal deductions, non-deposit of PF.
   - Statutory provisions: **Payment of Wages Act, 1936**; Industrial Disputes Act, 1947; Employees' Provident Funds Act, 1952.
   - Redressal mechanisms: Ministry of Labour **Samadhan Portal**, Labour Commissioner, **EPFiGMS**, and **Tele-Law**.

4. **Tenancy & Rental Disputes**
   - Unjustified withholding of security deposits, unlawful eviction threats, arbitrary utility shutoffs (water/power).
   - Statutory provisions: **Model Tenancy Act, 2021** (recommends maximum 2-month residential deposit cap; *note: as a central model framework, local enforcement is subject to respective State Government enactments and State Rent Control Acts*); Transfer of Property Act, 1882 (Sec 106 mandatory written notice); BNS 2023 (Sec 316 - Criminal Breach of Trust, Sec 329 - Criminal Trespass).
   - Redressal mechanisms: Local **Rent Authority / Rent Tribunal**, DLSA, Tele-Law.

5. **RTI (Right to Information) Assistance**
   - Delayed government scholarships, pending pensions, municipal project inquiries, official grievance tracking.
   - Statutory provisions: **Right to Information Act, 2005** (Sec 6(1) Request, Sec 7(1) 30-day timeline, Sec 19(1) First Appeal).
   - Portals: **rtionline.gov.in** (nominal statutory fee of ₹10, free for BPL applicants), Central Information Commission (CIC).

6. **State-Wise Legal Aid Locator (19 States & UTs)**
   - Tailored SLSA (State Legal Services Authority) contacts, state cyber wings, state consumer commissions, and free legal aid income eligibility thresholds.

---

## ⚡ High-Efficiency Architecture Upgrades

- **In-Memory LRU Caching**: Preloads and caches category knowledge structures in memory via `@functools.lru_cache`, eliminating synchronous disk reads per request.
- **Deterministic Response Caching**: Normalized SHA-256 query caching in SQLite (`response_cache`) returns verified answers in **<15ms** for frequent citizen inquiries, dramatically slashing external LLM costs and latency. Clean user isolation guarantees citizen details (name, state, query ID) are never leaked across cached responses.
- **Voice-to-Text Input (Web Speech API)**: Accessibility feature allowing citizens to describe their legal issues by speaking in Hindi (`hi-IN`) or English (`en-IN`).
- **Interactive Evidence Checklist & Progress Counter**: Itemized evidence tracker showing real-time readiness percentage.
- **Official Print / PDF Petition Generator**: Generates formatted petitions on standardized A4 margins with reference numbers and verification signatures, ready for physical filing at police stations, consumer commissions, or rent courts.
- **Citizen Legal Dossier & Checklist Downloads**: Exports plain-text dossiers and BSA 2023 Section 63 evidentiary checklists for physical presentation or offline records.
- **Header-Based API Security**: Uses `x-goog-api-key` request headers to ensure API keys are never exposed in URL query parameters or server access logs.

---

## 📁 Repository Structure

```text
ai legal/
│
├── app.py                  # Main Flask application, API routing & security controls
├── database.py             # SQLite setup, seeding, query storage & isolated cache
├── ai_service.py           # Strict RAG generator, header-auth APIs & offline fallback
├── legal_retriever.py      # Category classifier, verified context & draft templates
├── test_nyayamitra.py      # Automated 16-point unit, security & safety test suite
├── requirements.txt        # Python dependencies
├── Dockerfile              # Production Python 3.11 container configuration
├── docker-compose.yml      # Container orchestration with persistent SQLite volume
├── .dockerignore           # Excludes development artifacts from Docker builds
├── .env.example            # Environment variables template
├── README.md               # Project documentation
│
├── data/                   # Verified statutory knowledge base (6 datasets)
│   ├── cyber_fraud.json        # Cyber & UPI fraud procedures & BNS sections
│   ├── consumer_issues.json    # Consumer protection procedures & e-Daakhil
│   ├── employment_issues.json  # Wages, PF & labour grievance procedures
│   ├── tenancy_issues.json     # Rent dispute, Model Tenancy Act & notices
│   ├── rti_assistance.json     # RTI filing, timelines & first appeals
│   └── state_legal_aid.json    # State legal aid authorities for 19 states/UTs
│
├── database/               # Local SQLite database
│   └── nyayamitra.db
│
├── templates/              # Jinja2 HTML templates
│   ├── index.html          # Problem intake form, voice input & category selector
│   ├── result.html         # Structured 7-part legal response, checklist & follow-up
│   ├── history.html        # Past query consultations & ratings audit
│   └── print_draft.html    # Print-ready formal legal petition formatted for A4
│
└── static/                 # Rich aesthetic UI assets
    ├── style.css           # Modern glassmorphism, responsive styles & printing
    └── script.js           # Bilingual state, Web Speech API, checklist counter & sharing
```

---

## ⚡ Quick Start & Setup

### 1. Prerequisites
- Python 3.10 or 3.11 installed.

### 2. Clone and Install
```bash
git clone <repo-url>
cd "ai legal"
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
```
*(Note: An external API key is completely optional. If left blank, NyayaMitra runs seamlessly using its verified offline RAG engine and statutory knowledge base).*

**Production Security Best Practice:**
Generate a cryptographically secure random secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Place this value in your `.env` as `SECRET_KEY`.

### 4. Run Automated Tests
```bash
python -m unittest test_nyayamitra.py
```

### 5. Launch Application Locally
```bash
python app.py
```
Open your browser and navigate to: **`http://localhost:5000`**

### 6. Docker Deployment (Optional)
```bash
docker compose up --build -d
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Home page intake form, category selection, and emergency banner |
| `POST` | `/ask` | Process citizen legal query, perform RAG, save record, and return guidance |
| `POST` | `/follow-up` | Interactive follow-up Q&A (e.g. police FIR refusal under BNSS 173(4), fee structures) |
| `POST` | `/generate-draft` | Generate customized formal complaint draft with applicant details |
| `POST` | `/scan-document` | Transaction receipt & dispute entity parser (regex extraction for amounts, UTR, dates) |
| `GET` | `/print-draft` | Render official print-ready petition formatted for A4 PDF export |
| `GET` | `/download-dossier/<id>` | Download complete plain-text Citizen Legal Dossier |
| `GET` | `/download-checklist/<id>` | Download itemized evidence preservation checklist with BSA 2023 notes |
| `GET` | `/api/all-states` | List 19 supported States and Union Territories for UI dropdown |
| `GET` | `/api/state-aid` | Retrieve State Legal Services Authority, state cyber cell, and consumer commission |
| `GET` | `/history` | View stored previous legal queries and ratings |
| `POST` | `/feedback` | Submit 1–5 star rating and comments for a consultation |
| `GET` | `/health` | Production health check (returns supported categories, cache status & DB connectivity) |

---

## 📜 Compliance, Accuracy & Safety Guardrails

- **Statutory Grounding over Hallucinations**: Responses are grounded in curated statutory datasets verified against India Code and central legislation.
- **BNSS Procedural Remedies**: Follow-up chat accurately cites BNSS 2023 Section 173(4) (written representation to SP/DCP upon FIR refusal) and Section 175(3) (Magistrate inquiry application).
- **Model Tenancy Act Context**: Recognizes that the Model Tenancy Act, 2021 is a central model framework; advice highlights that state-specific rent enactments and municipal rules govern tenancy disputes locally.
- **Zero Financial Data Harvesting**: Never requests or stores banking passwords, Aadhaar, OTPs, or CVVs.
- **Disclaimers & NALSA Referral**: All responses, dossiers, and drafted complaints prominently clarify that the tool provides procedural legal information, not formal advocate representation. Direct escalation links to NALSA (15100) and Tele-Law (14488) are provided.
