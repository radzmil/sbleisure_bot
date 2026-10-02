"""Regression checks for publicly exposed Zulfa Bot routes."""
import hashlib
import hmac
import os
import json
import tempfile
import unittest
from unittest.mock import patch

os.environ.setdefault("PORTAL_API_KEY", "test-portal-key")
os.environ.setdefault("META_APP_SECRET", "test-meta-secret")

from app import app


class SecurityTests(unittest.TestCase):
    def setUp(self):
        self.portal_key = patch("app.PORTAL_API_KEY", "test-portal-key")
        self.meta_secret = patch("app.META_APP_SECRET", "test-meta-secret")
        self.portal_key.start()
        self.meta_secret.start()
        self.addCleanup(self.meta_secret.stop)
        self.addCleanup(self.portal_key.stop)
        self.client = app.test_client()

    def test_api_fails_closed_without_key_configuration(self):
        with patch("app.PORTAL_API_KEY", ""):
            response = self.client.get("/api/get-chat-history?phone=601234")
        self.assertEqual(response.status_code, 503)

    def test_api_rejects_missing_and_invalid_key(self):
        for headers in ({}, {"X-API-Key": "invalid"}):
            with self.subTest(headers=headers):
                self.assertEqual(self.client.get("/api/get-chat-history", headers=headers).status_code, 401)

    def test_api_accepts_correct_key(self):
        with patch("app.load_json_db", return_value=[]):
            response = self.client.get("/api/get-chat-history", headers={"X-API-Key": "test-portal-key"})
        self.assertEqual(response.status_code, 200)

    def test_webhook_requires_secret_and_valid_signature(self):
        body = b'{"entry": []}'
        with patch("app.META_APP_SECRET", ""):
            self.assertEqual(self.client.post("/webhook", data=body).status_code, 503)
        self.assertEqual(self.client.post("/webhook", data=body).status_code, 403)
        signature = "sha256=" + hmac.new(b"test-meta-secret", body, hashlib.sha256).hexdigest()
        with patch("app.dapatkan_client_id_dari_token", return_value=None):
            response = self.client.post("/webhook", data=body, headers={"X-Hub-Signature-256": signature, "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 200)

    def test_sheet_endpoint_removed(self):
        self.assertEqual(self.client.get("/test-sheet").status_code, 404)

    def test_repeated_meta_message_does_not_send_twice(self):
        body = json.dumps({"entry": [{"changes": [{"value": {"messages": [
            {"id": "wamid.test-1", "from": "60111111111", "type": "text", "text": {"body": "Hai"}}
        ]}}]}]}).encode()
        signature = "sha256=" + hmac.new(b"test-meta-secret", body, hashlib.sha256).hexdigest()
        headers = {"X-Hub-Signature-256": signature, "Content-Type": "application/json"}
        with tempfile.TemporaryDirectory() as directory, \
             patch("app.WEBHOOK_DEDUP_DB", os.path.join(directory, "dedup.db")), \
             patch("app.dapatkan_client_id_dari_token", return_value=None), \
             patch("app.save_message_to_postgres"), \
             patch("app.load_json_db", return_value=[{"phone": "+60111111111", "mode": "ai", "messages": []}]), \
             patch("app.save_json_db"), \
             patch("app.semak_mod_supabase", return_value="ai"), \
             patch("app.allow_ai_reply", return_value=True), \
             patch("app.zulfa_brain.jana_jawapan", return_value="Salam"), \
             patch("app.hantar_teks_whatsapp") as send, \
             patch("app.push_chat_to_sheets"), \
             patch("app.tolak_token_klien"):
            self.assertEqual(self.client.post("/webhook", data=body, headers=headers).status_code, 200)
            duplicate = self.client.post("/webhook", data=body, headers=headers)
            self.assertEqual(duplicate.status_code, 200)
            self.assertEqual(duplicate.json["reason"], "duplicate message")
            send.assert_called_once()

    def test_pause_stops_processing(self):
        body = b'{"entry": []}'
        signature = "sha256=" + hmac.new(b"test-meta-secret", body, hashlib.sha256).hexdigest()
        with patch.dict(os.environ, {"BOT_PAUSED": "1"}), patch("app.dapatkan_client_id_dari_token") as lookup:
            response = self.client.post("/webhook", data=body, headers={
                "X-Hub-Signature-256": signature, "Content-Type": "application/json"})
            self.assertEqual(response.json["status"], "paused")
            lookup.assert_not_called()

    def test_reply_cooldown(self):
        from app import allow_ai_reply
        with tempfile.TemporaryDirectory() as directory, \
             patch("app.WEBHOOK_DEDUP_DB", os.path.join(directory, "dedup.db")), \
             patch.dict(os.environ, {"AI_REPLY_COOLDOWN_SECONDS": "120"}):
            self.assertTrue(allow_ai_reply("60111111111"))
            self.assertFalse(allow_ai_reply("60111111111"))
            self.assertTrue(allow_ai_reply("60122222222"))


if __name__ == "__main__":
    unittest.main()