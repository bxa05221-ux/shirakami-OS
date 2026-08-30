from runtime.oppai_schema import normalize, to_dict


def test_oppai_preserves_raw_input_and_corrections():
    text = "これは操作摩擦の話なんだ。いや、そういう意味じゃない。人間がAIに合わせなくていいという話だ。"
    result = normalize(text)

    assert result.raw_input == text
    assert result.corrections == ("いや、そういう意味じゃない。",)
    assert result.confidence == "provisional"
    assert result.canonical_prompt == text


def test_oppai_separates_positive_interaction_from_fact():
    result = normalize("最高だ。まだ仮説だけど、実装してみよう。")

    assert result.interaction_signals == ("positive_interaction",)
    assert result.confidence == "observed"
    assert result.canonical_prompt == result.raw_input


def test_oppai_marks_questions_as_unresolved():
    result = normalize("これって本当にSchemaになるのか？")

    assert result.unresolved == ("これって本当にSchemaになるのか？",)
    assert result.confidence == "provisional"


def test_oppai_serialization_is_plain_data():
    result = to_dict(normalize("普通に話していい。"))

    assert result["raw_input"] == "普通に話していい。"
    assert result["canonical_prompt"] == "普通に話していい。"
    assert result["confidence"] == "observed"
