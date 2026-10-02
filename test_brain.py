"""Checks for conversation context and duplicate-answer correction."""
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import zulfa_brain


class BrainTests(unittest.TestCase):
    def test_system_prompt_has_one_behavior_section_and_single_engine_copy(self):
        with patch.object(zulfa_brain.sbleisure_engine, "get_engine_rules_text", return_value="UNIQUE_ENGINE_RULE"):
            prompt = zulfa_brain.bina_system_instruction()
        self.assertEqual(prompt.count("UNIQUE_ENGINE_RULE"), 1)
        self.assertEqual(prompt.count("=== PANDUAN NADA & PERILAKU ==="), 1)
        self.assertIn("Jangan ulang jawapan atau soalan terdahulu", prompt)
        self.assertNotIn("KLIA ke Ipoh, harga adalah RM1,780", prompt)

    def test_repeated_answer_is_rewritten_using_history(self):
        history = [{"role": "user", "content": "Ada bas?"},
                   {"role": "assistant", "content": "Ada bas."}]
        model = SimpleNamespace(models=SimpleNamespace(generate_content=lambda **kwargs: None))
        with patch.object(zulfa_brain, "client", model), \
             patch.object(zulfa_brain, "dapatkan_konteks_pelanggan", return_value={"sejarah_mesej": history}), \
             patch.object(zulfa_brain, "bina_system_instruction", return_value="instructions"), \
             patch.object(zulfa_brain, "kemaskini_konteks_pelanggan") as save, \
             patch.object(model.models, "generate_content", side_effect=[
                 SimpleNamespace(text="Ada bas."), SimpleNamespace(text="Ya, bas tersedia. Tarikh bila?")]) as generate:
            self.assertEqual(zulfa_brain.proses_mesej("6011", "Bas untuk esok?"),
                             "Ya, bas tersedia. Tarikh bila?")
            self.assertEqual(generate.call_count, 2)
            self.assertEqual(generate.call_args_list[0].kwargs["contents"][1].role, "model")
            save.assert_called_once()


if __name__ == "__main__":
    unittest.main()