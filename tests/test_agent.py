import json
import unittest
from pathlib import Path
from unittest.mock import patch
from io import BytesIO

from src.main import ROOT, ChatModel, KnowledgeBase, MockModel, run, validate_finish


class AgentTests(unittest.TestCase):
    def case(self, name, data="documents.json", max_steps=8):
        payload = json.loads((ROOT / "examples" / (name + ".input.json")).read_text(encoding="utf-8"))
        return run(payload, KnowledgeBase(ROOT / "data" / data, payload.get("fail_tools", [])), MockModel(), max_steps)

    def test_clear_answer(self):
        out = self.case("clear")
        self.assertEqual(out["status"], "answered")
        self.assertEqual(out["citations"][0]["id"], "D03")
        self.assertIn("2GB", out["answer"])

    def test_conflict(self):
        out = self.case("conflict")
        self.assertEqual(out["status"], "conflict")
        self.assertEqual({x["id"] for x in out["citations"]}, {"D01", "D02"})
        self.assertIn("适用", out["answer"])

    def test_outside(self):
        self.assertEqual(self.case("outside")["status"], "insufficient")

    def test_paraphrase(self):
        self.assertEqual(self.case("paraphrase")["status"], "answered")

    def test_followup(self):
        self.assertEqual(self.case("followup")["status"], "answered")

    def test_tool_failure(self):
        out = self.case("failure")
        self.assertEqual(out["status"], "insufficient")
        self.assertTrue(any("error" in x for x in out["trace"]))

    def test_single_document_changes_answer(self):
        out = self.case("conflict", "single-document.json")
        self.assertEqual(out["status"], "answered")
        self.assertIn("30天", out["answer"])

    def test_step_limit(self):
        self.assertEqual(self.case("clear", max_steps=1)["status"], "incomplete")

    def test_unread_citation_rejected(self):
        with self.assertRaises(ValueError):
            validate_finish({"status": "answered", "answer": "2GB", "citations": [{"id": "D03", "quote": "伪造"}], "gap": ""}, {}, [])

    def test_unread_conflict_candidate_rejected(self):
        kb = KnowledgeBase(ROOT / "data" / "documents.json")
        d = kb.read("D01")
        with self.assertRaises(ValueError):
            validate_finish({"status": "answered", "answer": "30天", "citations": [{"id": "D01", "quote": d["text"]}], "gap": ""}, {"D01": d}, kb.search("报销期限"))

    def test_chat_tool_call_protocol(self):
        response = {"choices": [{"message": {"content": None, "tool_calls": [{"id": "call-1", "type": "function", "function": {"name": "search_documents", "arguments": '{"query":"报销期限"}'}}]}}]}
        class Reply(BytesIO):
            def __enter__(self):
                return self
            def __exit__(self, *args):
                self.close()
        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-only", "OPENAI_MODEL": "test-model"}), patch("urllib.request.urlopen", return_value=Reply(json.dumps(response).encode())) as opened:
            name, args, assistant, call_id = ChatModel().choose([{"role": "user", "content": "报销期限"}])
            sent = json.loads(opened.call_args.args[0].data)
        self.assertEqual((name, args, call_id), ("search_documents", {"query": "报销期限"}, "call-1"))
        self.assertEqual(sent["tool_choice"], "required")
        self.assertFalse(sent["parallel_tool_calls"])
        self.assertEqual(assistant["tool_calls"][0]["id"], "call-1")


if __name__ == "__main__":
    unittest.main()
