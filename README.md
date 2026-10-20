# NyayaMitra AI (न्यायमित्र)
> **Simple, Safe and Accessible Legal Information for Every Indian**

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/framework-Flask%203.1-black.svg)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/database-SQLite-lightgrey.svg)](https://www.sqlite.org/)
[![Status](https://img.shields.io/badge/MVP-Verified%20under%20India%20Code-green.svg)](https://www.indiacode.nic.in/)

NyayaMitra AI is an Indian legal-information assistant designed to empower citizens by translating complex procedural laws into clear, empathetic, and actionable guidance. It recommends official government grievance resources, delivers interactive evidence checklists, and generates customizable formal complaint drafts in **English** and **Hindi**.

---

## 🎯 Hackathon Scope: 3 Focused MVP Categories

To ensure 100% legal correctness and prevent hallucinations during hackathon demonstrations, NyayaMitra AI focuses deeply on three high-impact civic domains:

1. **Cyber & Financial Fraud**
   - UPI scams, OTP fraud, phishing links, unauthorized bank debits, fake loan apps, impersonation.
   - Statutory provisions: **Information Technology Act, 2000** (Sec 66C, 66D); **Bharatiya Nyaya Sanhita (BNS), 2023** (Sec 318 - Cheating, Sec 319 - Cheating by personation).
   - Emergency response: Immediate freeze within "Golden Hour" via **1930 Helpline** & [cybercrime.gov.in](https://cybercrime.gov.in).

2. **Consumer Complaints & Disputes**
   - Defective goods, delivery damages, refused refunds, false advertising, e-commerce service deficiency.
   - Statutory provisions: **Consumer Protection Act, 2019**; E-Commerce Rules, 2020.
   - Government portals: **National Consumer Helpline (NCH 1915)**, **INGRAM**, and **e-Daakhil** online commission filing.

3. **Workplace & Salary Issues**
   - Unpaid wages, delayed salaries, withheld relieving letters, illegal deductions, non-deposit of PF.
   - Statutory provisions: **Payment of Wages Act, 1936**; Industrial Disputes Act, 1947; EPF Act, 1952.
   - Redressal mechanisms: Ministry of Labour **Samadhan Portal**, Labour Commissioner, **EPFiGMS**, and **Tele-Law**.

---

## 🏛️ Grounded in India Code & BNS 2023

NyayaMitra AI uses **India Code** as its authoritative primary source for central and state legislation:
- **No Hallucinated Sections**: Legal provisions are verified and anchored in structured knowledge files.
- **BNS 2023 Transition**: Criminal provisions reference the **Bharatiya Nyaya Sanhita, 2023** (effective July 1, 2024), actively deprecating outdated IPC references (e.g., citing BNS Sec 318 rather than old IPC Sec 420).
- **Zero-Downtime Offline Fallback**: Even without an external LLM API key or active internet, the built-in deterministic RAG engine reliably synthesizes verified legal guidance.

---

## 🚀 Key Features

1. **Intelligent Legal Problem Classifier**: Automatically detects whether an issue is cyber fraud, a consumer dispute, or a workplace issue from freeform natural language text in English or Hindi.
2. **Fixed 7-Part Output Architecture**:
   - `Problem Category`
   - `Simple Plain-Language Explanation`
   - `Immediate Actions` (Prioritized step-by-step)
   - `Interactive Evidence Checklist` (Dynamic checkboxes to track readiness)
   - `Official Resources & Emergency Helplines` (Direct toll-free dials & portal links)
   - `Editable Complaint Draft Generator` (Customizable with applicant details, dates, and amounts)
   - `Statutory Safety Disclaimer` (Non-guarantee warning & DLSA / Tele-Law referral)
3. **Bilingual English & Hindi Engine**: Seamless UI and procedural content toggling between English and Hindi.
4. **Local Audit History & Feedback**: Secure SQLite query history for auditing previous queries without retaining sensitive financial credentials (passwords, OTPs, CVVs).

---

## 🏗️ System Architecture

```text
       User (Citizen)
             │
             ▼
     Web Interface (HTML5 / Vanilla CSS / Modern JS)
             │
             ▼
       Flask Backend (app.py)
             │
   ┌─────────┴────────────────────────┐
   ▼                                  ▼
Category Classifier              Legal Knowledge Retriever (data/*.json)
(detect_category)               (Anchored to India Code & Helplines)
   │                                  │
   └─────────┬────────────────────────┘
             ▼
     Strict RAG Prompt Builder
             │
     ┌───────┴────────────────────────┐
     ▼                                ▼
AI Provider (Gemini / OpenAI)    Deterministic Offline Fallback
     └───────┬────────────────────────┘
             ▼
    Structured JSON Output Validation
             │
             ▼
  SQLite Database (database/nyayamitra.db)
  [legal_resources | legal_queries | feedback]
```

---

## 📁 Repository Structure

```text
nyayamitra-ai/
│
├── app.py                  # Main Flask application & routing
├── database.py             # SQLite setup, seeding, and query management
├── ai_service.py           # Strict RAG generator with offline fallback
├── legal_retriever.py      # Category detector & verified template engine
├── test_nyayamitra.py      # Automated 9-point unit & safety test suite
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── README.md               # Project documentation
│
├── data/                   # Verified legal knowledge base
│   ├── cyber_fraud.json
│   ├── consumer_issues.json
│   └── employment_issues.json
│
├── database/               # Local SQLite database
│   └── nyayamitra.db
│
├── templates/              # Jinja2 HTML templates
│   ├── index.html          # Problem intake form & emergency banner
│   ├── result.html         # Structured 7-part legal response & checklist
│   └── history.html        # Past query consultations
│
└── static/                 # Rich aesthetic UI assets
    ├── style.css           # Glassmorphism, animations, responsive design
    └── script.js           # Bilingual state, clipboard, checklist counter
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

### 3. Configure Environment (Optional)
```bash
cp .env.example .env
```
*(Note: An API key is optional. If left blank, NyayaMitra runs smoothly using its verified offline RAG engine).*

### 4. Run Automated Tests
```bash
python test_nyayamitra.py
```

### 5. Launch Application
```bash
python app.py
```
Open your browser and navigate to: **`http://localhost:5000`**

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Home page intake form & category selector |
| `POST` | `/ask` | Process legal query, perform RAG, save record, and return guidance |
| `POST` | `/generate-draft` | Generate customized formal complaint draft |
| `GET` | `/history` | View stored previous legal queries and ratings |
| `POST` | `/feedback` | Submit 1–5 star rating and comments for a query |
| `GET` | `/health` | Check API, database, and knowledge base status |

---

## 🎤 2-Minute Demo Script for Judges

1. **Introduction (15 sec)**:
   > *"Millions of Indian citizens face cyber frauds, rejected refunds, or unpaid wages every month, but get paralyzed by legal jargon and confusing procedures. NyayaMitra AI is a verified first-step legal guidance assistant that turns complex statutes into immediate, actionable steps."*

2. **Demonstration (60 sec)**:
   - Click the quick demo pill: *"₹5,000 deducted after clicking fake UPI link"*.
   - Point out automatic categorization into **Cyber & Financial Fraud**.
   - Show the **Immediate Actions** highlighting the critical **1930 Golden Hour helpline**.
   - Interact with the **Documents & Evidence Checklist** (check off bank statement and screenshot).
   - Display the **Enforced Legislation** showing **Bharatiya Nyaya Sanhita (BNS) 2023 Section 318**.
   - Scroll to the **Complaint Draft Generator**: click *Customize Details* to input the victim's name/amount and click *Copy Draft* or *Print*.
   - Toggle to **Hindi (हिंदी)** to demonstrate equal accessibility for non-English speakers.

3. **Conclusion & Safety (30 sec)**:
   > *"NyayaMitra does not replace a lawyer and never gives false outcome guarantees. It bridges the critical pre-litigation gap by preserving evidence and directly connecting citizens to official statutory platforms like cybercrime.gov.in, NALSA, and Tele-Law."*

---

## 📜 Compliance & Safety Guardrails
- **No Hallucinated Precedents**: Responses are strictly bound to verified government datasets.
- **Zero Data Harvesting**: Never stores banking passwords, Aadhaar, OTPs, or CVVs.
- **Statutory Disclaimers**: Prominently highlights that content is general legal information and encourages consulting Legal Aid Clinics (NALSA 15100).
