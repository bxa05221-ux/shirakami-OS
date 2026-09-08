from runtime.context_sheet import load_context_sheet


def test_context_sheet_preserves_human_authored_landscape_fields():
    landscape = {
        "sheet_id": "nursery-001",
        "observations": ["AくんがBちゃんの誘いで遊びに参加した。"],
        "assessments": ["参加のきっかけに他児との関係が影響している可能性がある。"],
        "unresolved_questions": ["次回も同じ関係が見られるだろうか。"],
        "planned_support": ["少人数で遊べる環境を用意する。"],
    }

    result = load_context_sheet(landscape)

    assert result.landscape == landscape
    assert result.observations == tuple(landscape["observations"])
    assert result.unresolved_questions == tuple(landscape["unresolved_questions"])
    assert "assessments" in result.landscape
    assert "planned_support" in result.landscape


def test_context_sheet_does_not_treat_missing_fields_as_facts():
    result = load_context_sheet({"sheet_id": "empty"})

    assert result.observations == ()
    assert result.unresolved_questions == ()


def test_context_sheet_ignores_non_string_items_without_rewriting_landscape():
    landscape = {
        "observations": ["観察1", 42, None],
        "unresolved_questions": ["問い1", False],
    }

    result = load_context_sheet(landscape)

    assert result.observations == ("観察1",)
    assert result.unresolved_questions == ("問い1",)
    assert result.landscape == landscape
