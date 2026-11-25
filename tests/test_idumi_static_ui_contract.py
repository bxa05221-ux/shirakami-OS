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


def test_bilingual_setting_is_present_and_used_in_prompt():
    source = HTML.read_text(encoding="utf-8")
    fields = Fields()
    fields.feed(source)
    assert fields.fields["bilingual"][0] == "select"
    assert 'value="ja-en"' in source
    assert '日本語の各レスに英語対訳を付ける' in source
    assert 'bilingual:state.bilingual' in source
    assert 'bilingual:String(x.bilingual||"ja-en")' in source


def test_thread_boundary_and_handoff_contract_statically_present():
    source = HTML.read_text(encoding="utf-8")
    assert 'max="1000"' in source
    assert "state.posts.length+out.length>1000" in source
    assert "state.posts.length>=950" in source
    assert "idumi-matome-candidate" in source
    assert "carryOver" in source
    assert "user_pasted_ai_output_unverified" in source
    assert 'kind:"op"' in source
    assert 'p.kind==="op"?"イッチ：":"名無しさん："' in source
    assert 'state.posts.length+i+1' in source


def test_no_api_keys_or_remote_script_in_static_launcher():
    source = HTML.read_text(encoding="utf-8")
    assert "<script src=" not in source
    assert "api.openai.com" not in source
    assert "sk-proj-" not in source
    assert "navigator.clipboard.writeText" in source
    assert "api.github.com/repos/" in source


def test_only_the_allowlisted_formal_protocol_is_attached_and_verified():
    source = HTML.read_text(encoding="utf-8")
    assert 'FORMAL_PROTOCOL={id:"thread-rpg-v1.2.1",path:"protocols/thread-rpg-v1.2.1.yaml",version:"1.2.1"}' in source
    assert 'const pairs=[[FORMAL_PROTOCOL.id,FORMAL_PROTOCOL.path]]' in source
    assert 'crypto.subtle.digest("SHA-1"' in source
    assert 'if(digest!==meta.sha)' in source
    assert '参照バージョン不一致' in source
    assert 'oppaiP' not in source


def test_prompt_preserves_anonymous_simulation_and_stop_boundary():
    source = HTML.read_text(encoding="utf-8")
    assert 'Play ThreadRPG as a Japanese 2channel-style anonymous forum.' in source
    assert 'not assigned characters or experts' in source
    assert '停止・中止を命じられたら直ちに生成を止める' in source
    assert '強制的な結論や総括は作らない' in source
    assert '群像劇' not in source
    assert '最大7つの意見に集約' not in source


def test_ai_generation_is_external_not_falsely_claimed():
    source = HTML.read_text(encoding="utf-8")
    assert "OPPAI Runtimeや非公開資産を実行・配布しません" in source
    assert "AI APIキーは不要です" in source
