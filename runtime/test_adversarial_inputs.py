"""Adversarial input checks for the β0.1 Matome loader.

These tests cover bounded, deterministic malformed-input cases only. They do
not claim full YAML parser or denial-of-service resistance.
"""

import unittest

from protocol_loader import ProtocolLoadError, parse_matome


class AdversarialInputTests(unittest.TestCase):
    def assert_rejected(self, text: str) -> None:
        with self.assertRaises(ProtocolLoadError):
            parse_matome(text)

    def test_empty_input_is_rejected(self):
        self.assert_rejected("")

    def test_wrong_root_is_rejected(self):
        self.assert_rejected("root:\n  title: invalid\n")

    def test_missing_statement_is_rejected(self):
        self.assert_rejected(
            """matome:
  title: Missing Statement
  version: 0.1
  pipeline:
    - phase: observe
      action: capture_input
"""
        )

    def test_empty_statement_is_rejected(self):
        self.assert_rejected(
            """matome:
  title: Empty Statement
  version: 0.1
  statement: >
  pipeline:
    - phase: observe
      action: capture_input
"""
        )

    def test_pipeline_item_without_action_is_rejected(self):
        self.assert_rejected(
            """matome:
  title: Missing Action
  version: 0.1
  statement: >
    A statement.
  pipeline:
    - phase: observe
"""
        )


if __name__ == "__main__":
    unittest.main()
