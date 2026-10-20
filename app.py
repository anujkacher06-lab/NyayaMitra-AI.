import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from dotenv import load_dotenv

import database
import legal_retriever
import ai_service

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "nyayamitra-secret-key-2026")

# Initialize database on app startup
database.init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        # Check if form submission or JSON
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

        # Step 1: Detect or map category
        detected_category = legal_retriever.detect_category(question, user_category)

        # Step 2: Retrieve verified legal context
        verified_ctx = legal_retriever.get_verified_context(detected_category, language)

        # Step 3 & 4: Safe AI synthesis with strict verified context & fallback
        response_data = ai_service.generate_legal_response(detected_category, question, verified_ctx, language)
        response_data["user_name"] = user_name
        response_data["state"] = state
        response_data["language"] = language
        response_data["category_id"] = detected_category

        # Step 5: Save query to SQLite
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

@app.route("/history")
def history():
    queries = database.get_queries(limit=50)
    # Parse responses for display
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
        "version": "1.0.0-mvp",
        "supported_categories": [
            "cyber_fraud",
            "consumer_complaint",
            "workplace_salary_issue"
        ],
        "primary_legislation_source": "India Code (Bharatiya Nyaya Sanhita 2023, CPA 2019, Payment of Wages Act)",
        "database": "SQLite connected",
        "ai_providers": {
            "gemini_configured": gemini_key,
            "openai_configured": openai_key,
            "verified_rag_offline_fallback": "Active & Ready"
        }
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
