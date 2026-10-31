import os
import json
import sqlite3
import hashlib
from datetime import datetime

DB_DIR = os.path.join(os.path.dirname(__file__), "database")
DB_PATH = os.path.join(DB_DIR, "nyayamitra.db")
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def get_db_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Legal resources table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS legal_resources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL UNIQUE,
        title TEXT NOT NULL,
        simple_explanation TEXT NOT NULL,
        actions_json TEXT NOT NULL,
        evidence_json TEXT NOT NULL,
        official_resource_name TEXT,
        official_resource_reference TEXT,
        verified_at TEXT NOT NULL
    );
    """)

    # 2. Citizen queries audit table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS legal_queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        question TEXT NOT NULL,
        language TEXT NOT NULL,
        response TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 3. User feedback table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query_id INTEGER NOT NULL,
        rating INTEGER,
        comments TEXT,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (query_id) REFERENCES legal_queries(id)
    );
    """)

    # 4. Response caching table for high efficiency & quota protection
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS response_cache (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cache_key TEXT NOT NULL UNIQUE,
        category TEXT NOT NULL,
        question TEXT NOT NULL,
        language TEXT NOT NULL,
        response_json TEXT NOT NULL,
        hit_count INTEGER DEFAULT 1,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_cache_key ON response_cache(cache_key);
    """)

    conn.commit()
    conn.close()
    seed_resources()

def seed_resources():
    files = {
        "cyber_fraud": "cyber_fraud.json",
        "consumer_complaint": "consumer_issues.json",
        "workplace_salary_issue": "employment_issues.json",
        "tenancy_dispute": "tenancy_issues.json",
        "rti_assistance": "rti_assistance.json"
    }

    conn = get_db_connection()
    cursor = conn.cursor()

    for cat_key, filename in files.items():
        filepath = os.path.join(DATA_DIR, filename)
        if not os.path.exists(filepath):
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        title = data.get("title", {}).get("en", cat_key)
        explanation = data.get("simple_explanation", {}).get("en", "")
        actions = json.dumps(data.get("immediate_actions", {}).get("en", []))
        evidence = json.dumps(data.get("evidence_checklist", {}).get("en", []))
        resources = data.get("official_resources", [])
        res_name = resources[0]["name"] if resources else "Official Portal"
        res_ref = resources[0]["url"] if resources else "https://cybercrime.gov.in"
        verified_at = data.get("verified_date", "2026-07-16")

        cursor.execute("""
        INSERT INTO legal_resources 
        (category, title, simple_explanation, actions_json, evidence_json, official_resource_name, official_resource_reference, verified_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(category) DO UPDATE SET
            title=excluded.title,
            simple_explanation=excluded.simple_explanation,
            actions_json=excluded.actions_json,
            evidence_json=excluded.evidence_json,
            official_resource_name=excluded.official_resource_name,
            official_resource_reference=excluded.official_resource_reference,
            verified_at=excluded.verified_at
        """, (cat_key, title, explanation, actions, evidence, res_name, res_ref, verified_at))

    conn.commit()
    conn.close()

def compute_cache_key(category: str, question: str, language: str) -> str:
    """
    Computes a deterministic hash of the normalized query for instant cache lookup.
    """
    normalized = f"{category.strip().lower()}|{language.strip().lower()}|{' '.join(question.strip().lower().split())}"
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

def get_cached_response(category: str, question: str, language: str):
    """
    Retrieves cached legal response if available, bumping the hit count.
    """
    key = compute_cache_key(category, question, language)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT response_json, hit_count FROM response_cache WHERE cache_key = ?
    """, (key,))
    row = cursor.fetchone()

    if row:
        cursor.execute("""
            UPDATE response_cache 
            SET hit_count = hit_count + 1, updated_at = CURRENT_TIMESTAMP 
            WHERE cache_key = ?
        """, (key,))
        conn.commit()
        conn.close()
        try:
            data = json.loads(row["response_json"])
            # Return sanitized legal analysis; strip any user-specific attributes
            data.pop("user_name", None)
            data.pop("state", None)
            data.pop("query_id", None)
            data["from_cache"] = True
            return data
        except Exception:
            return None

    conn.close()
    return None

def set_cached_response(category: str, question: str, language: str, response_data: dict):
    """
    Stores an AI legal response into the persistent SQLite cache.
    Ensures user-specific details (name, state, query_id) are NOT stored in the shared cache.
    """
    key = compute_cache_key(category, question, language)
    # Sanitize payload: cache only statutory legal synthesis, not user profile or state aid
    clean_data = dict(response_data)
    for user_key in ("user_name", "state", "state_aid", "query_id", "from_cache"):
        clean_data.pop(user_key, None)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO response_cache (cache_key, category, question, language, response_json)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(cache_key) DO UPDATE SET
            response_json = excluded.response_json,
            updated_at = CURRENT_TIMESTAMP
    """, (key, category, question, language, json.dumps(clean_data, ensure_ascii=False)))
    conn.commit()
    conn.close()

def save_query(category: str, question: str, language: str, response: str) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO legal_queries (category, question, language, response, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (category, question, language, response, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    query_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return query_id

def get_queries(limit: int = 50):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT q.id, q.category, q.question, q.language, q.response, q.created_at,
               f.rating, f.comments
        FROM legal_queries q
        LEFT JOIN feedback f ON q.id = f.query_id
        ORDER BY q.id DESC
        LIMIT ?
    """, (limit,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_query_by_id(query_id):
    try:
        qid = int(query_id)
    except (ValueError, TypeError):
        return None

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, category, question, language, response, created_at
        FROM legal_queries
        WHERE id = ?
    """, (qid,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def save_feedback(query_id: int, rating: int, comments: str = "") -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO feedback (query_id, rating, comments, created_at)
        VALUES (?, ?, ?, ?)
    """, (query_id, rating, comments, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    feedback_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return feedback_id

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at", DB_PATH)
