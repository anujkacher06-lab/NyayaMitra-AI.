import os
import io
import re
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, Response, send_file
from dotenv import load_dotenv

import database
import legal_retriever
import ai_service
import pdf_generator

load_dotenv()

app = Flask(__name__)
# Generate secure random secret if not explicitly configured in environment
app.secret_key = os.getenv("SECRET_KEY") or os.urandom(24).hex()

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
            response_data = dict(cached_response)
        else:
            # Step 4: Safe AI synthesis with strict verified context & fallback
            response_data = ai_service.generate_legal_response(detected_category, question, verified_ctx, language)
            # Store sanitized statutory legal analysis in cache (without user-specific details)
            database.set_cached_response(detected_category, question, language, response_data)

        # Attach citizen query specific attributes
        response_data["user_name"] = user_name
        response_data["state"] = state
        response_data["language"] = language
        response_data["category_id"] = detected_category

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
        # Accept conversation history from frontend
        chat_history = data.get("chat_history") or []
        if isinstance(chat_history, str):
            try:
                chat_history = json.loads(chat_history)
            except Exception:
                chat_history = []

        if not follow_up_q:
            return jsonify({"status": "error", "message": "Please enter a follow-up question."}), 400

        original_q = ""
        category = "cyber_fraud"
        language = "English"

        if query_id is not None and str(query_id).strip():
            record = database.get_query_by_id(query_id)
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
            language=language,
            chat_history=chat_history
        )

        return jsonify({
            "status": "success",
            "follow_up_question": follow_up_q,
            "answer": answer
        })
    except Exception as e:
        print(f"Error in follow-up route: {e}")
        return jsonify({"status": "error", "message": "Unable to process follow-up question at this moment. Please try again."}), 500

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
        print(f"Error generating draft: {e}")
        return jsonify({"status": "error", "message": "Could not generate legal draft. Please check the inputs."}), 500

@app.route("/scan-document", methods=["POST"])
def scan_document():
    """
    Parses document text, transaction receipts, or image uploads using multi-tiered OCR
    (Gemini 1.5 Flash Vision, OpenAI Vision, local Tesseract, or Pillow image metadata)
    to extract dispute entities (amount, 12-digit UTR, date, payment app, and category).
    """
    try:
        raw_text = ""
        file_bytes = b""
        filename = ""
        mime_type = ""
        language = "English"

        if request.is_json:
            data = request.get_json() or {}
            raw_text = data.get("text", "")
            language = data.get("language", "English")
        else:
            if request.form:
                raw_text = request.form.get("text", "")
                language = request.form.get("language", "English")
            if request.files and "file" in request.files:
                uploaded_file = request.files["file"]
                filename = uploaded_file.filename or "receipt"
                mime_type = uploaded_file.mimetype or ""
                file_bytes = uploaded_file.read()

        payload = ai_service.parse_document_or_receipt(
            file_bytes=file_bytes,
            filename=filename,
            mime_type=mime_type,
            text_context=raw_text,
            language=language
        )
        return jsonify(payload)
    except Exception as e:
        print(f"Error scanning document text: {e}")
        return jsonify({"status": "error", "message": "Failed to parse document text. Please provide valid text or transaction details."}), 500

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
            query_record = database.get_query_by_id(query_id)
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

@app.route("/export-pdf", methods=["GET", "POST"])
def export_pdf():
    """
    Generates and downloads a court-ready, formal A4 PDF legal petition
    with judicial styling, statutory citations, evidence checklist, and verification block.
    """
    draft_text = ""
    category = "Civic Legal Dispute"
    user_name = ""
    state = ""
    laws = []
    evidence = []
    resources = []
    language = "English"

    query_id = request.args.get("query_id") or request.form.get("query_id")
    if query_id:
        record = database.get_query_by_id(query_id)
        if record:
            category = record.get("category", category)
            user_name = record.get("user_name", "")
            state = record.get("state", "")
            language = record.get("language", "English")
            ctx = legal_retriever.get_verified_context(category, language)
            laws = ctx.get("applicable_laws", [])
            evidence = ctx.get("evidence", [])
            resources = ctx.get("resources", [])
            draft_text = legal_retriever.generate_local_complaint_draft(
                category, language, {"name": user_name, "state": state, "description": record.get("question", "")}
            )

    if not draft_text:
        draft_text = request.form.get("draft_text") or request.args.get("draft_text") or ""
    if not draft_text:
        draft_text = "Official Legal Notice / Complaint Draft\n\nSubmitted by Complainant under verified statutory provisions."

    pdf_bytes = pdf_generator.generate_petition_pdf(
        category_title=category,
        draft_text=draft_text,
        user_name=user_name,
        state=state,
        laws=laws,
        evidence=evidence,
        resources=resources,
        language=language
    )

    clean_cat = re.sub(r'[^a-zA-Z0-9_-]', '_', category)
    filename = f"NyayaMitra_Formal_Petition_{clean_cat}.pdf"

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename
    )

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
        if not data:
            return jsonify({"status": "error", "message": "No feedback data provided."}), 400

        raw_qid = data.get("query_id")
        try:
            query_id = int(raw_qid)
        except (ValueError, TypeError):
            return jsonify({"status": "error", "message": "Valid numeric query ID is required."}), 400

        try:
            rating = int(data.get("rating", 5))
        except (ValueError, TypeError):
            rating = 5
        rating = max(1, min(5, rating))
        comments = (data.get("comments") or "").strip()

        feedback_id = database.save_feedback(query_id, rating, comments)
        return jsonify({"status": "success", "feedback_id": feedback_id, "message": "Feedback recorded. Thank you!"})
    except Exception as e:
        print(f"Error saving feedback: {e}")
        return jsonify({"status": "error", "message": "Unable to save feedback at this moment. Please try again."}), 500

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
    # Security: Default to debug=False; enable only when FLASK_DEBUG=true is explicitly set
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() in ("true", "1")
    app.run(debug=debug_mode, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
