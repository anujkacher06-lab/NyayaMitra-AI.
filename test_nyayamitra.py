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

    def test_14_cache_user_isolation(self):
        # User A makes a query
        resp_a = self.client.post("/ask", json={
            "question": "Electricity bill scam SMS deducted funds",
            "category": "cyber_fraud",
            "language": "English",
            "user_name": "Aarav Sharma",
            "state": "Maharashtra"
        })
        self.assertEqual(resp_a.status_code, 200)
        data_a = resp_a.get_json()
        self.assertEqual(data_a["user_name"], "Aarav Sharma")
        self.assertEqual(data_a["state"], "Maharashtra")
        qid_a = data_a["query_id"]

        # User B makes identical query with different name and state (hits cache)
        resp_b = self.client.post("/ask", json={
            "question": "Electricity bill scam SMS deducted funds",
            "category": "cyber_fraud",
            "language": "English",
            "user_name": "Bhavna Patel",
            "state": "Gujarat"
        })
        self.assertEqual(resp_b.status_code, 200)
        data_b = resp_b.get_json()
        self.assertTrue(data_b.get("from_cache"))
        self.assertEqual(data_b["user_name"], "Bhavna Patel")
        self.assertEqual(data_b["state"], "Gujarat")
        qid_b = data_b["query_id"]
        self.assertNotEqual(qid_a, qid_b, "Distinct query records must be created for each user")

        # Verify raw cached response in DB does not leak user names
        cached_raw = database.get_cached_response("cyber_fraud", "Electricity bill scam SMS deducted funds", "English")
        self.assertNotIn("user_name", cached_raw, "Cache must not store citizen identity")
        self.assertNotIn("state", cached_raw, "Cache must not store citizen state")

    def test_15_robust_error_handling_and_non_numeric_ids(self):
        # Non-numeric query_id in follow-up should not crash with 500
        resp_fu = self.client.post("/follow-up", json={
            "query_id": "invalid-non-numeric-id",
            "question": "How long will this process take?"
        })
        self.assertEqual(resp_fu.status_code, 200)
        self.assertIn("answer", resp_fu.get_json())

        # Non-numeric query_id in print-draft should not crash
        resp_pd = self.client.get("/print-draft?query_id=invalid_id")
        self.assertEqual(resp_pd.status_code, 200)

        # Non-numeric query_id in feedback should return clean 400 error without exception trace
        resp_fb = self.client.post("/feedback", json={
            "query_id": "not_an_int",
            "rating": 5
        })
        self.assertEqual(resp_fb.status_code, 400)
        fb_json = resp_fb.get_json()
        self.assertEqual(fb_json["status"], "error")
        self.assertNotIn("Traceback", fb_json["message"])

    def test_16_scan_document_entity_extraction(self):
        # Text input parsing
        receipt_text = "Paid ₹14,500 via UPI. UTR Ref No: 412345678901 on 15/07/2026 for damaged electronics."
        resp = self.client.post("/scan-document", json={"text": receipt_text})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["status"], "success")
        entities = data["entities"]
        self.assertEqual(entities["amount"], "14,500")
        self.assertEqual(entities["utr"], "412345678901")
        self.assertEqual(entities["incident_date"], "15/07/2026")
        self.assertIn(entities["detected_category"], ["cyber_fraud", "consumer_complaint"])

        # Binary/image upload notice
        import io
        fake_image = (io.BytesIO(b"fake image data"), "screenshot.png")
        resp_img = self.client.post(
            "/scan-document",
            data={"file": fake_image},
            content_type="multipart/form-data"
        )
        self.assertEqual(resp_img.status_code, 200)
        img_data = resp_img.get_json()
        self.assertEqual(img_data["status"], "success")
        self.assertIn("note", img_data)

    def test_17_ocr_vision_and_image_pipeline(self):
        import io
        from unittest.mock import patch
        from PIL import Image

        # 1. Real PIL image upload (fallback / Pillow Image Inspector)
        img_buf = io.BytesIO()
        test_img = Image.new("RGB", (320, 240), color="white")
        test_img.save(img_buf, format="PNG")
        img_buf.seek(0)

        resp = self.client.post(
            "/scan-document",
            data={
                "file": (img_buf, "payment_slip.png"),
                "text": "Sent money ₹20,000 to fake landlord UTR: 555666777888 on 20/08/2026",
                "language": "English"
            },
            content_type="multipart/form-data"
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["status"], "success")
        self.assertIn("320x240", data.get("note", ""))
        self.assertEqual(data["entities"]["amount"], "20,000")
        self.assertEqual(data["entities"]["utr"], "555666777888")
        self.assertEqual(data["entities"]["incident_date"], "20/08/2026")
        self.assertTrue(len(data.get("auto_fill_prompt", "")) > 10)

        # 2. Mock Gemini 1.5 Flash Vision OCR
        mock_vision_data = {
            "extracted_text": "PhonePe Successful. Paid ₹35,000 to ABC Real Estate. UTR: 998877665544. Date: 12/09/2026.",
            "amount": "35,000",
            "utr": "998877665544",
            "incident_date": "12/09/2026",
            "payment_app": "PhonePe",
            "sender_or_victim": "Rahul Verma",
            "recipient_or_accused": "ABC Real Estate",
            "detected_category": "tenancy_dispute",
            "summary": "Tenant paid security deposit of ₹35,000 via PhonePe on 12/09/2026 to ABC Real Estate with UTR 998877665544."
        }
        with patch("ai_service.query_gemini_vision", return_value=mock_vision_data):
            with patch.dict("os.environ", {"GEMINI_API_KEY": "dummy_test_key"}):
                img_buf2 = io.BytesIO()
                test_img.save(img_buf2, format="PNG")
                img_buf2.seek(0)

                resp_v = self.client.post(
                    "/scan-document",
                    data={"file": (img_buf2, "receipt.png"), "language": "English"},
                    content_type="multipart/form-data"
                )
                self.assertEqual(resp_v.status_code, 200)
                v_data = resp_v.get_json()
                self.assertEqual(v_data["status"], "success")
                self.assertEqual(v_data["ocr_engine"], "Gemini 1.5 Flash Vision")
                self.assertEqual(v_data["entities"]["amount"], "35,000")
                self.assertEqual(v_data["entities"]["utr"], "998877665544")
                self.assertEqual(v_data["entities"]["detected_category"], "tenancy_dispute")
                self.assertIn("Tenant paid security deposit", v_data["auto_fill_prompt"])

        # 3. Hindi auto-fill prompt generation
        hi_entities = {
            "amount": "5,000",
            "utr": "123456789012",
            "incident_date": "01/10/2026",
            "payment_app": "Google Pay",
            "detected_category": "cyber_fraud"
        }
        hi_prompt = ai_service.build_auto_fill_prompt(hi_entities, language="Hindi")
        self.assertIn("₹5,000", hi_prompt)
        self.assertIn("123456789012", hi_prompt)
        self.assertIn("1930", hi_prompt)

    def test_18_pdf_generator_and_export_route(self):
        """Test server-side formal petition PDF generation and /export-pdf route."""
        import pdf_generator
        pdf_bytes = pdf_generator.generate_petition_pdf(
            category_title="Cyber & Financial Fraud",
            draft_text="To,\nThe Inspector of Police,\nCyber Crime Cell...\n\nPrayer: Kindly register FIR and freeze beneficiary account.",
            user_name="Anuj Sharma",
            state="Delhi",
            laws=["Bharatiya Nyaya Sanhita, 2023 (Sec 318(4))", "Information Technology Act, 2000 (Sec 66D)"],
            evidence=["Bank Statement showing debit", "Transaction UTR acknowledgment screenshot"],
            resources=[{"name": "National Cyber Helpline", "contact": "1930"}]
        )
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertTrue(pdf_bytes.startswith(b"%PDF"), "Output must be a valid PDF starting with %PDF")
        self.assertGreater(len(pdf_bytes), 1000)

        # Test Flask /export-pdf route
        resp = self.client.get("/export-pdf?draft_text=Official+Legal+Notice&category=cyber_fraud")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("Content-Type"), "application/pdf")
        self.assertTrue(resp.data.startswith(b"%PDF"))

    def test_19_telegram_bot_formatting(self):
        """Test Telegram bot response formatting and structure."""
        import telegram_bot
        mock_res = {
            "category": "Consumer Complaints",
            "explanation": "You received a defective smartphone and merchant refused refund.",
            "actions": ["Issue legal notice", "File complaint on NCH 1915", "Approach e-Daakhil"],
            "evidence": ["Purchase invoice", "Unboxing video"],
            "applicable_laws": ["Consumer Protection Act, 2019"],
            "official_resources": [{"name": "National Consumer Helpline", "contact": "1915"}],
            "disclaimer": "This is general civic legal information, not professional legal advice."
        }
        msg = telegram_bot.format_telegram_response(mock_res)
        self.assertIn("NyayaMitra Legal Guidance", msg)
        self.assertIn("Consumer Complaints", msg)
        self.assertIn("Consumer Protection Act, 2019", msg)
        self.assertIn("1915", msg)
        self.assertIn("Disclaimer", msg)

    def test_20_whatsapp_notice_formatting(self):
        """Test WhatsApp legal notice URL generation in Telegram bot."""
        import telegram_bot
        mock_res = {
            "category": "Tenancy Disputes",
            "explanation": "Landlord refusing to refund deposit of 140000.",
            "actions": ["Send statutory demand notice under Model Tenancy Act"],
            "official_resources": [{"name": "Rent Authority", "contact": "State SLSA"}],
            "disclaimer": "Safety legal disclaimer"
        }
        msg = telegram_bot.format_telegram_response(mock_res)
        self.assertIn("Send Formal Notice via WhatsApp", msg)
        self.assertIn("https://api.whatsapp.com/send?text=", msg)
        self.assertIn("Section%2063%20BSA%202023", msg)

if __name__ == "__main__":
    unittest.main()
