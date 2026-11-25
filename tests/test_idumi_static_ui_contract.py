"""Static contract checks for standalone IDUMI launcher.

These do not replace live browser interaction or LLM behavior tests.
"""
from pathlib import Path
from html.parser import HTMLParser

HTML = Path(__file__).resolve().parents[1] / "experiments" / "idumi" / "index.html"


class Fields(HTMLParser):
    def __init__(self):
        super().__init__()
        self.fields = {}

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if "id" in data:
            self.fields[data["id"]] = (tag, data)


def test_idumi_required_slider_limits_and_ids():
    source = HTML.read_text(encoding="utf-8")
    fields = Fields()
    fields.feed(source)
    for name, minimum, maximum in (
        ("members", "1", "7"),
        ("replies", "1", "10"),
        ("closeness", "0", "100"),
        ("language", "0", "100"),
    ):
        tag, field = fields.fields[name]
        assert tag == "input"
        assert field["type"] == "range"
        assert field["min"] == minimum
        assert field["max"] == maximum
    assert 'id="seed"' in source
    assert 'id="aiOutput"' in source


def test_initial_product_is_explicitly_selected_and_uses_formal_protocol():
    source = HTML.read_text(encoding="utf-8")
    fields = Fields()
    fields.feed(source)
    tag, field = fields.fields["product"]
    assert tag == "select"
    assert 'value="thread-rpg-v1.2.1"' in source
    assert 'protocols/thread-rpg-v1.2.1.yaml' in source
    assert 'function selectedProduct()' in source


def test_thread_boundary_and_handoff_contract_statically_present():
    source = HTML.read_text(encoding="utf-8")
    assert 'max="1000"' in source
    assert "state.posts.length+out.length>1000" in source
    assert "state.posts.length>=950" in source
    assert "idumi-matome-candidate" in source
    assert "carryOver" in source
    assert "user_pasted_ai_output_unverified" in source


def test_no_api_keys_or_remote_script_in_static_launcher():
    source = HTML.read_text(encoding="utf-8")
    assert "<script src=" not in source
    assert "api.openai.com" not in source
    assert "sk-proj-" not in source
    assert "navigator.clipboard.writeText" in source
    assert "api.github.com/repos/" in source


def test_ai_generation_is_external_not_falsely_claimed():
    source = HTML.read_text(encoding="utf-8")
    assert "OPPAI Runtime自体を実行するものではありません" in source
    assert "AI APIキーは不要です" in source
