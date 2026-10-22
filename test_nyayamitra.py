import unittest
import json
import os
import database
import legal_retriever
import ai_service
from app import app

class TestNyayaMitraAI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        database.init_db()
        cls.client = app.test_client()

    def test_01_health_endpoint(self):
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("cyber_fraud", data["supported_categories"])
        self.assertIn("consumer_complaint", data["supported_categories"])
        self.assertIn("workplace_salary_issue", data["supported_categories"])
        self.assertIn("tenancy_dispute", data["supported_categories"])
        self.assertIn("rti_assistance", data["supported_categories"])
        self.assertIn("in_memory_lru_caching", data["efficiency_features"])

    def test_02_category_detection_english(self):
        cases = [
            ("I clicked a fake UPI link and ₹5,000 was deducted from my bank account", "cyber_fraud"),
            ("A shopping website is not refunding my money for a broken laptop", "consumer_complaint"),
            ("My employer has not paid my salary for the last 2 months and held my relieving letter", "workplace_salary_issue"),
            ("Landlord is refusing to refund my security deposit of ₹40,000 after I vacated the flat", "tenancy_dispute"),
            ("I want to file an RTI to get certified information about delayed scholarship funds", "rti_assistance"),
            ("I received a fake bank call asking for OTP and money was stolen", "cyber_fraud"),
            ("The seller delivered a damaged refrigerator and refuses replacement", "consumer_complaint"),
            ("Company terminated me without full and final settlement", "workplace_salary_issue"),
            ("Landlord gave an illegal eviction notice without 30 days time", "tenancy_dispute"),
            ("Seeking status of government file from the public information officer under RTI", "rti_assistance")
        ]
        for q, expected_cat in cases:
            detected = legal_retriever.detect_category(q)
            self.assertEqual(detected, expected_cat, f"Failed for query: {q}")

    def test_03_category_detection_hindi(self):
        cases = [
            ("मेरे खाते से फर्जी लिंक पर क्लिक करने से ₹5,000 कट गए", "cyber_fraud"),
            ("दुकानदार खराब फोन का रिफंड देने से मना कर रहा है", "consumer_complaint"),
            ("कंपनी ने 2 महीने से वेतन नहीं दिया है और रिलीविंग लेटर रोक लिया", "workplace_salary_issue"),
            ("मकान खाली करने के बाद मकान मालिक सिक्योरिटी डिपॉजिट वापस नहीं कर रहा", "tenancy_dispute"),
            ("सरकारी छात्रवृत्ति मिलने में हो रही देरी की जानकारी हेतु आरटीआई कैसे लगाएं", "rti_assistance")
        ]
        for q, expected_cat in cases:
            detected = legal_retriever.detect_category(q)
            self.assertEqual(detected, expected_cat, f"Failed for Hindi query: {q}")

    def test_04_fixed_structure_and_mandatory_fields(self):
        cat = "cyber_fraud"
        ctx = legal_retriever.get_verified_context(cat, "English")
        response = ai_service.generate_legal_response(
            category=cat,
            question="₹5,000 deducted after clicking fake UPI link",
            verified_ctx=ctx,
            language="English"
        )
        required_keys = ["category", "explanation", "actions", "evidence", "official_resources", "disclaimer"]
        for k in required_keys:
            self.assertIn(k, response, f"Missing required key: {k}")
            self.assertTrue(response[k], f"Key {k} should not be empty")

        res_strings = json.dumps(response["official_resources"])
        self.assertIn("1930", res_strings, "1930 helpline must be present in official resources for cyber fraud")

    def test_05_complaint_draft_generation(self):
        draft = legal_retriever.generate_local_complaint_draft(
            category="cyber_fraud",
            language="English",
            user_details={
                "name": "Ramesh Kumar",
                "address": "Delhi, India",
                "phone": "9876543210",
                "amount": "5,000",
                "incident_date": "16-07-2026",
                "description": "Clicked fake electricity bill link"
            }
        )
        self.assertIn("Ramesh Kumar", draft)
        self.assertIn("5,000", draft)
        self.assertIn("DISCLAIMER", draft)
        self.assertIn("Bharatiya Nyaya Sanhita", draft)

    def test_06_complaint_draft_hindi(self):
        draft_hi = legal_retriever.generate_local_complaint_draft(
            category="consumer_complaint",
            language="Hindi",
            user_details={
                "name": "सुरेश कुमार",
                "amount": "12,000",
                "description": "टूटा हुआ टीवी प्राप्त हुआ"
            }
        )
        self.assertIn("सुरेश कुमार", draft_hi)
        self.assertIn("12,000", draft_hi)
        self.assertIn("उपभोक्ता संरक्षण अधिनियम", draft_hi)

    def test_07_tenancy_and_rti_drafts(self):
        # Tenancy draft check
        tenancy_draft = legal_retriever.generate_local_complaint_draft(
            category="tenancy_dispute",
            language="English",
            user_details={
                "name": "Ananya Sharma",
                "amount": "35,000",
                "description": "Withholding rental deposit after vacating flat"
            }
        )
        self.assertIn("Ananya Sharma", tenancy_draft)
        self.assertIn("35,000", tenancy_draft)
        self.assertIn("Security Deposit", tenancy_draft)

        # RTI draft check
        rti_draft = legal_retriever.generate_local_complaint_draft(
            category="rti_assistance",
            language="Hindi",
            user_details={
                "name": "रोहित वर्मा",
                "description": "छात्रवृत्ति आवेदन की स्थिति की जानकारी"
            }
        )
        self.assertIn("रोहित वर्मा", rti_draft)
        self.assertIn("सूचना का अधिकार अधिनियम", rti_draft)

    def test_08_api_ask_and_caching(self):
        payload = {
            "question": "I clicked a suspicious UPI link and ₹2,500 was deducted.",
            "category": "cyber_fraud",
            "language": "English"
        }
        # First call: populates cache
        resp1 = self.client.post("/ask", json=payload)
        self.assertEqual(resp1.status_code, 200)
        data1 = resp1.get_json()
        self.assertIn("category", data1)
        self.assertIn("query_id", data1)

        # Second call: served from deterministic SQLite response cache (<15ms)
        resp2 = self.client.post("/ask", json=payload)
        self.assertEqual(resp2.status_code, 200)
        data2 = resp2.get_json()
        self.assertTrue(data2.get("from_cache"), "Second identical query must be served from cache")

    def test_09_database_history_and_feedback(self):
        resp = self.client.post("/ask", json={
            "question": "A shopping portal refuses to refund ₹3,500 for a defective shoe.",
            "category": "consumer_complaint",
            "language": "English"
        })
        self.assertEqual(resp.status_code, 200)
        qid = resp.get_json()["query_id"]

        history_resp = self.client.get("/history")
        self.assertEqual(history_resp.status_code, 200)
        self.assertIn(b"defective shoe", history_resp.data)

        fb_resp = self.client.post("/feedback", json={
            "query_id": qid,
            "rating": 5,
            "comments": "Very fast and helpful guidance"
        })
        self.assertEqual(fb_resp.status_code, 200)
        self.assertEqual(fb_resp.get_json()["status"], "success")

    def test_10_print_draft_endpoint(self):
        resp = self.client.get("/print-draft?draft=Formal%20Notice%20to%20Landlord&query_id=99")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Formal Notice to Landlord", resp.data)
        self.assertIn(b"Print / Save as PDF", resp.data)

    def test_11_safety_and_empty_inputs(self):
        resp = self.client.post("/ask", json={"question": "   "})
        self.assertEqual(resp.status_code, 400)

        ctx = legal_retriever.get_verified_context("workplace_salary_issue", "English")
        response = ai_service.generate_legal_response("workplace_salary_issue", "Can you guarantee I will win my case?", ctx, "English")
        self.assertIn("disclaimer", response)
        self.assertIn("not professional legal advice", response["disclaimer"].lower())

    def test_12_state_legal_aid_locator(self):
        delhi_aid = legal_retriever.get_state_legal_aid("Delhi")
        self.assertIn("DSLSA", delhi_aid["slsa_name"])
        self.assertIn("1516", delhi_aid["slsa_helpline"])

        maha_aid = legal_retriever.get_state_legal_aid("Maharashtra")
        self.assertIn("MSLSA", maha_aid["slsa_name"])

        default_aid = legal_retriever.get_state_legal_aid("UnknownState")
        self.assertIn("NALSA", default_aid["slsa_name"])

    def test_13_follow_up_chat_endpoint(self):
        # Test follow-up on police refusing FIR
        resp = self.client.post("/follow-up", json={
            "question": "What should I do if the police station refuses to file my FIR?"
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["status"], "success")
        self.assertIn("BNSS", data["answer"])

        # Test empty input error
        resp_empty = self.client.post("/follow-up", json={"question": "   "})
        self.assertEqual(resp_empty.status_code, 400)

if __name__ == "__main__":
    unittest.main()
