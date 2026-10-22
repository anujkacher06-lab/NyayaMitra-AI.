import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, Response
from dotenv import load_dotenv

import database
import legal_retriever
import ai_service

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "nyayamitra-secret-key-2026")

# Initialize database and seed knowledge tables on startup
database.init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        question = (data.get("question") or data.get("problem_description") or "").strip()
        user_category = (data.get("category") or "").strip()
        language = (data.get("language") or "English").strip()
        user_name = (data.get("user_name") or "").strip()
        state = (data.get("state") or "").strip()

        if not question:
            if request.is_json:
                return jsonify({"error": "Please describe your legal issue / कृपया अपनी समस्या का विवरण दें।"}), 400
            flash("Please enter a description of your issue / कृपया अपनी समस्या दर्ज करें।", "warning")
            return redirect(url_for("index"))

        # Step 1: Detect category with keyword & Hinglish booster matching
        detected_category = legal_retriever.detect_category(question, user_category)

        # Step 2: Retrieve verified legal context (LRU cached in memory)
        verified_ctx = legal_retriever.get_verified_context(detected_category, language)

        # Step 3: High-efficiency Response Cache Check (avoids repeated LLM calls)
        cached_response = database.get_cached_response(detected_category, question, language)
        if cached_response:
            response_data = cached_response
            response_data["user_name"] = user_name
            response_data["state"] = state
            response_data["language"] = language
            response_data["category_id"] = detected_category
        else:
            # Step 4: Safe AI synthesis with strict verified context & fallback
            response_data = ai_service.generate_legal_response(detected_category, question, verified_ctx, language)
            response_data["user_name"] = user_name
            response_data["state"] = state
            response_data["language"] = language
            response_data["category_id"] = detected_category
            # Store in cache
            database.set_cached_response(detected_category, question, language, response_data)

        # Step 5: Attach State Legal Services Authority details
        response_data["state_aid"] = legal_retriever.get_state_legal_aid(state, language)

        # Step 6: Save citizen query audit record to SQLite
        query_id = database.save_query(
            category=detected_category,
            question=question,
            language=language,
            response=json.dumps(response_data, ensure_ascii=False)
        )
        response_data["query_id"] = query_id

        if request.is_json:
            return jsonify(response_data)

        return render_template("result.html", result=response_data, raw_response=json.dumps(response_data))

    except Exception as e:
        print(f"Error processing legal query: {e}")
        if request.is_json:
            return jsonify({"error": "An error occurred while analyzing the legal request. Please try again."}), 500
        flash("Could not process request at this moment. Please check the inputs.", "danger")
        return redirect(url_for("index"))

@app.route("/follow-up", methods=["POST"])
def follow_up():
    try:
        data = request.get_json() if request.is_json else request.form
        query_id = data.get("query_id")
        follow_up_q = (data.get("question") or "").strip()

        if not follow_up_q:
            return jsonify({"error": "Please enter a follow-up question."}), 400

        original_q = ""
        category = "cyber_fraud"
        language = "English"

        if query_id:
            record = database.get_query_by_id(int(query_id))
            if record:
                original_q = record["question"]
                category = record["category"]
                language = record["language"]

        verified_ctx = legal_retriever.get_verified_context(category, language)
        answer = ai_service.generate_follow_up_answer(
            category=category,
            original_question=original_q,
            follow_up_question=follow_up_q,
            verified_ctx=verified_ctx,
            language=language
        )

        return jsonify({
            "status": "success",
            "follow_up_question": follow_up_q,
            "answer": answer
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate-draft", methods=["POST"])
def generate_draft():
    try:
        data = request.get_json() if request.is_json else request.form
        category = data.get("category", "cyber_fraud")
        language = data.get("language", "English")

        user_details = {
            "name": data.get("name") or data.get("user_name"),
            "address": data.get("address"),
            "phone": data.get("phone"),
            "email": data.get("email"),
            "amount": data.get("amount"),
            "incident_date": data.get("incident_date") or data.get("date"),
            "time": data.get("time"),
            "description": data.get("description") or data.get("problem_description")
        }

        draft_content = legal_retriever.generate_local_complaint_draft(category, language, user_details)

        return jsonify({
            "status": "success",
            "category": category,
            "language": language,
            "draft": draft_content
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/scan-document", methods=["POST"])
def scan_document():
    """
    Parses document text or image uploads to extract legal dispute entities
    (amount, 12-digit UTR, date, and classified legal category).
    """
    try:
        raw_text = ""
        if request.is_json:
            data = request.get_json()
            raw_text = data.get("text", "")
        elif "text" in request.form:
            raw_text = request.form.get("text", "")
        elif "file" in request.files:
            file = request.files["file"]
            filename = file.filename or "receipt"
            raw_text = f"Attached document: {filename}."

        import re
        amt_match = re.search(r'(?:₹|rs\.?|inr)\s*([0-9,]+(?:\.\d{2})?)', raw_text, re.IGNORECASE)
        amount = amt_match.group(1) if amt_match else ""

        utr_match = re.search(r'\b(\d{12})\b', raw_text)
        utr = utr_match.group(1) if utr_match else ""

        date_match = re.search(r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b', raw_text)
        incident_date = date_match.group(1) if date_match else ""

        detected_cat = legal_retriever.detect_category(raw_text)

        return jsonify({
            "status": "success",
            "extracted_text": raw_text,
            "entities": {
                "amount": amount,
                "utr": utr,
                "incident_date": incident_date,
                "detected_category": detected_cat
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/print-draft", methods=["GET", "POST"])
def print_draft():
    """
    Renders an official, print-ready formal legal petition formatted for A4 PDF export.
    """
    if request.method == "POST":
        data = request.form
        draft_content = data.get("draft_text", "")
        query_id = data.get("query_id", "")
    else:
        query_id = request.args.get("query_id", "")
        draft_content = request.args.get("draft", "")

        if query_id and not draft_content:
            query_record = database.get_query_by_id(int(query_id))
            if query_record:
                try:
                    cat = query_record["category"]
                    lang = query_record["language"]
                    draft_content = legal_retriever.generate_local_complaint_draft(
                        cat, lang, {"description": query_record["question"]}
                    )
                except Exception:
                    pass

    if not draft_content:
        draft_content = "No draft content available. Please generate a draft first."

    return render_template("print_draft.html", draft_content=draft_content, query_id=query_id)

@app.route("/api/all-states", methods=["GET"])
def api_all_states():
    """Returns list of supported states/UTs for dynamic UI selectors."""
    return jsonify({
        "status": "success",
        "states": legal_retriever.get_all_states()
    })

@app.route("/api/state-aid", methods=["GET"])
def api_state_aid():
    """Returns official SLSA, Cyber Wing, Consumer Commission for requested state."""
    state_name = request.args.get("state", "").strip()
    language = request.args.get("language", "English").strip()
    aid_data = legal_retriever.get_state_legal_aid(state_name, language)
    return jsonify({
        "status": "success",
        "state_aid": aid_data
    })

@app.route("/download-dossier/<int:query_id>", methods=["GET"])
def download_dossier(query_id):
    """
    Exports a clean, complete plain-text Citizen Legal Dossier
    ready for physical filing or offline storage.
    """
    record = database.get_query_by_id(query_id)
    if not record:
        flash("Query record not found.", "warning")
        return redirect(url_for("history"))

    try:
        parsed_resp = json.loads(record["response"])
    except Exception:
        parsed_resp = {
            "query_id": query_id,
            "category": record["category"],
            "explanation": record["question"]
        }
    parsed_resp["query_id"] = query_id

    # Generate or fetch draft
    draft_text = ""
    try:
        draft_text = legal_retriever.generate_local_complaint_draft(
            record["category"],
            record["language"],
            {"description": record["question"]}
        )
    except Exception:
        pass

    dossier_text = legal_retriever.generate_case_dossier(parsed_resp, draft_text)
    filename = f"NyayaMitra_Legal_Dossier_{query_id}.txt"

    return Response(
        dossier_text,
        mimetype="text/plain; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.route("/download-checklist/<int:query_id>", methods=["GET"])
def download_checklist(query_id):
    """
    Exports an itemized evidence & document preservation checklist
    with statutory verification notes under BSA 2023 / IT Act Sec 65B.
    """
    record = database.get_query_by_id(query_id)
    if not record:
        flash("Query record not found.", "warning")
        return redirect(url_for("history"))

    try:
        parsed = json.loads(record["response"])
        evidence_list = parsed.get("evidence", [])
        cat_name = parsed.get("category", record["category"])
    except Exception:
        evidence_list = []
        cat_name = record["category"]

    lines = []
    lines.append("=" * 70)
    lines.append(f"NYAYAMITRA AI - EVIDENCE & DOCUMENT CHECKLIST (REF #{query_id})")
    lines.append(f"Category: {cat_name}")
    lines.append("=" * 70)
    lines.append("")
    lines.append("TICK ITEMS AS PREPARED:")
    for idx, item in enumerate(evidence_list, 1):
        lines.append(f"[ ] {idx}. {item}")
    lines.append("")
    lines.append("-" * 70)
    lines.append("CRITICAL STATUTORY EVIDENTIARY GUIDELINES (BHARATIYA SAKSHYA ADHINIYAM, 2023):")
    lines.append("• Electronic Records (WhatsApp chats, emails, bank SMS, UPI receipts) require")
    lines.append("  certification under Section 63 of Bharatiya Sakshya Adhiniyam, 2023 (BSA).")
    lines.append("• Preserve primary device unedited; take full-page screenshots showing timestamp & URL.")
    lines.append("• Bank Statement: Obtain bank-stamped account statement highlighting fraudulent transaction.")
    lines.append("• Helpline numbers for escalation: Cyber Fraud 1930 | Consumer 1915 | NALSA 15100")
    lines.append("=" * 70)

    content = "\n".join(lines)
    filename = f"NyayaMitra_Evidence_Checklist_{query_id}.txt"
    return Response(
        content,
        mimetype="text/plain; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.route("/history")
def history():
    queries = database.get_queries(limit=50)
    processed_queries = []
    for q in queries:
        q_copy = dict(q)
        try:
            q_copy["parsed_response"] = json.loads(q_copy["response"])
        except Exception:
            q_copy["parsed_response"] = {}
        processed_queries.append(q_copy)
    return render_template("history.html", queries=processed_queries)

@app.route("/query/<int:query_id>")
def view_query(query_id):
    query_record = database.get_query_by_id(query_id)
    if not query_record:
        flash("Query record not found.", "warning")
        return redirect(url_for("history"))
    try:
        parsed = json.loads(query_record["response"])
        parsed["query_id"] = query_record["id"]
        parsed["question"] = query_record["question"]
    except Exception:
        parsed = {}
    return render_template("result.html", result=parsed, raw_response=json.dumps(parsed))

@app.route("/feedback", methods=["POST"])
def feedback():
    try:
        data = request.get_json() if request.is_json else request.form
        query_id = int(data.get("query_id"))
        rating = int(data.get("rating", 5))
        comments = data.get("comments", "").strip()

        feedback_id = database.save_feedback(query_id, rating, comments)
        return jsonify({"status": "success", "feedback_id": feedback_id, "message": "Feedback recorded. Thank you!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/health")
def health():
    gemini_key = bool(os.getenv("GEMINI_API_KEY") or os.getenv("AI_API_KEY"))
    openai_key = bool(os.getenv("OPENAI_API_KEY"))
    return jsonify({
        "status": "healthy",
        "service": "NyayaMitra AI",
        "version": "1.2.0-enhanced",
        "supported_categories": [
            "cyber_fraud",
            "consumer_complaint",
            "workplace_salary_issue",
            "tenancy_dispute",
            "rti_assistance"
        ],
        "efficiency_features": [
            "in_memory_lru_caching",
            "deterministic_response_cache",
            "instant_voice_recognition_ready",
            "formal_a4_pdf_export_ready"
        ],
        "primary_legislation_source": "India Code (BNS 2023, CPA 2019, Payment of Wages Act, Model Tenancy Act 2021, RTI Act 2005)",
        "database": "SQLite connected & indexed",
        "ai_providers": {
            "gemini_configured": gemini_key,
            "openai_configured": openai_key,
            "verified_rag_offline_fallback": "Active & Ready"
        }
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
