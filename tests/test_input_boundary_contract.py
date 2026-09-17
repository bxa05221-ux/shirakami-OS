import pytest

from runtime.oppai_schema import normalize, to_dict


def test_input_boundary_preserves_japanese_unicode_and_newlines():
    text = "第一行。\nいや、そこではない。\n未解決なのか？"

    observation = normalize(text)

    assert observation.raw_input == text
    assert observation.canonical_prompt == text
    assert to_dict(observation)["raw_input"] == text
    assert to_dict(observation)["canonical_prompt"] == text


def test_input_boundary_keeps_observation_separate_from_source_text():
    text = "最高だ。これは仮説？"

    observation = normalize(text)

    assert observation.raw_input is text
    assert observation.canonical_prompt is text
    assert observation.interaction_signals == ("positive_interaction",)
    assert observation.unresolved == ("これは仮説？",)


@pytest.mark.parametrize("value", ["", "   ", None, 123])
def test_input_boundary_rejects_empty_or_invalid_input(value):
    with pytest.raises(ValueError):
        normalize(value)
