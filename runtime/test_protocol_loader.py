"""Tests for the β0.1 Matome loader."""

import tempfile
import unittest
from pathlib import Path

from protocol_loader import ProtocolLoadError, load_matome


VALID = """matome:
  title: Test Protocol
  version: 0.1
  statement: >
    A test protocol.
  pipeline:
    - phase: observe
      action: capture_input
    - phase: evidence
      action: capture_evidence
"""


class ProtocolLoaderTests(unittest.TestCase):
    def test_load_valid_matome(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "protocol.yaml"
            path.write_text(VALID, encoding="utf-8")
            protocol = load_matome(path)

        self.assertEqual(protocol.title, "Test Protocol")
        self.assertEqual(protocol.version, "0.1")
        self.assertEqual(protocol.protocol_id, "test.protocol")
        self.assertEqual(protocol.pipeline[0]["phase"], "observe")

    def test_rejects_missing_root(self):
        with self.assertRaises(ProtocolLoadError):
            from protocol_loader import parse_matome
            parse_matome("title: invalid\n")

    def test_rejects_pipeline_without_action(self):
        with self.assertRaises(ProtocolLoadError):
            from protocol_loader import parse_matome
            parse_matome(
                """matome:\n  title: Broken\n  version: 0.1\n  statement: >\n    Broken\n  pipeline:\n    - phase: observe\n"""
            )


if __name__ == "__main__":
    unittest.main()
