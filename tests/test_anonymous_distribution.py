from runtime.thread_rpg import AnonymousOpinion, ThreadRenderer, allocate_anonymous_counts


def test_weighted_distribution_with_minority_preservation():
    opinions = [
        AnonymousOpinion("a", "main", 0.80),
        AnonymousOpinion("b", "minor", 0.15),
        AnonymousOpinion("c", "small", 0.05),
    ]

    counts = allocate_anonymous_counts(opinions, preserve_minority=True)

    assert sum(counts.values()) == 7
    assert counts["a"] >= counts["b"] >= counts["c"]
    assert counts["b"] >= 1
    assert counts["c"] >= 1


def test_anonymous_group_size_is_fixed_at_seven():
    opinions = [
        AnonymousOpinion("a", "main", 1.0),
        AnonymousOpinion("b", "none", 0.0),
    ]

    rendered = ThreadRenderer.render_anonymous_group(opinions)

    assert len(rendered) == 7
    assert all(item["opinion_id"] == "a" for item in rendered)


def test_renderer_keeps_opinion_text_and_does_not_change_weight_meaning():
    opinions = [
        AnonymousOpinion("a", "first", 0.8),
        AnonymousOpinion("b", "second", 0.2),
    ]

    rendered = ThreadRenderer.render_anonymous_group(opinions)

    assert len(rendered) == 7
    assert {item["text"] for item in rendered} == {"first", "second"}
    assert {item["opinion_id"] for item in rendered} == {"a", "b"}
