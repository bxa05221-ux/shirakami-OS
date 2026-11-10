"""A local-only desktop trial app for third-party evaluators.

No account, network client, external model, or persistent storage is used.
Closing the app discards the synthetic trial entries from memory.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tkinter as tk
from tkinter import messagebox, ttk

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from products.tokyo_welfare_evaluation_prototype import (
    ConsensusRecord,
    EvaluatorInput,
    SyntheticCase,
    TokyoWelfareEvaluationTrial,
    TrialBoundaryError,
    TrialFeedback,
)


EVALUATORS = ("評価者A", "評価者B")


def new_trial() -> TokyoWelfareEvaluationTrial:
    return TokyoWelfareEvaluationTrial(
        SyntheticCase(
            "synthetic-tokyo-welfare-trial-001",
            "架空の通所介護事業所 ひだまり",
            "通所介護（架空）",
            "公式資料の評価手順を練習するための、実在者を含まない架空案件です。",
        ),
        set(EVALUATORS),
    )


class TrialDesktopApp:
    """Small GUI that exposes only the synthetic, human-gated trial workflow."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("第三者評価 支援AI・架空案件試用版")
        self.root.minsize(860, 620)
        self.trial = new_trial()
        self.records_by_evaluator: dict[str, list[tuple[str, str]]] = {person: [] for person in EVALUATORS}
        self._build()

    def _build(self) -> None:
        notice = tk.Label(
            self.root,
            text="架空データ限定 / 外部送信なし / AIは最終判断をしません / アプリを閉じると入力内容は消えます",
            foreground="#9b1c1c", anchor="w", padx=12, pady=8,
        )
        notice.pack(fill="x")
        tabs = ttk.Notebook(self.root)
        tabs.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.guide_tab = ttk.Frame(tabs, padding=14)
        self.input_tab = ttk.Frame(tabs, padding=14)
        self.compare_tab = ttk.Frame(tabs, padding=14)
        self.consensus_tab = ttk.Frame(tabs, padding=14)
        self.feedback_tab = ttk.Frame(tabs, padding=14)
        tabs.add(self.guide_tab, text="1. 試用の案内")
        tabs.add(self.input_tab, text="2. 根拠を入力")
        tabs.add(self.compare_tab, text="3. 比較・共有")
        tabs.add(self.consensus_tab, text="4. 合議・草案")
        tabs.add(self.feedback_tab, text="5. 試用の感想")
        self._build_guide()
        self._build_input()
        self._build_compare()
        self._build_consensus()
        self._build_feedback()

    @staticmethod
    def _text(parent: ttk.Frame, *, height: int = 16) -> tk.Text:
        widget = tk.Text(parent, wrap="word", height=height, font=("Yu Gothic UI", 10))
        widget.pack(fill="both", expand=True)
        return widget

    def _build_guide(self) -> None:
        text = self._text(self.guide_tab)
        instructions = self.trial.manual_guided_trial()
        reference = instructions["official_reference"]
        body = [
            "このアプリは、第三者評価の経験者が架空案件で操作感を試すためのものです。",
            "実在の事業所名、利用者情報、評価記録、アンケート結果を入力しないでください。",
            "",
            "参照する公式資料",
            f"・{reference['title']}",
            f"・ガイドブック: {reference['source_url']}",
            f"・最新様式: {reference['forms_url']}",
            "",
            "試用の進め方",
        ]
        body.extend(f"{step['step_id']}. {step['manual_topic']} — {step['trial_action']}" for step in instructions["steps"])
        body.extend(("", "最終的な評価、評点、講評の確定は、このアプリでは行いません。"))
        text.insert("1.0", "\n".join(body))
        text.configure(state="disabled")

    def _build_input(self) -> None:
        frame = self.input_tab
        ttk.Label(frame, text="評価者").pack(anchor="w")
        self.input_evaluator = ttk.Combobox(frame, values=EVALUATORS, state="readonly")
        self.input_evaluator.set(EVALUATORS[0])
        self.input_evaluator.pack(fill="x", pady=(0, 8))
        self.criterion = self._entry(frame, "評価観点（例: 利用者本位の支援）")
        self.observation = self._entry(frame, "架空資料からの観察")
        self.evidence = self._entry(frame, "根拠（複数の場合は改行で区切る）", multiline=True)
        self.tentative = self._entry(frame, "暫定的な見解")
        ttk.Button(frame, text="この評価者だけの記録として保存", command=self.save_input).pack(anchor="e", pady=10)
        self.input_status = ttk.Label(frame, text="保存後、本人が共有を選ぶまで他の評価者には表示されません。")
        self.input_status.pack(anchor="w")

    def _entry(self, parent: ttk.Frame, label: str, multiline: bool = False):
        ttk.Label(parent, text=label).pack(anchor="w", pady=(6, 0))
        if multiline:
            field = tk.Text(parent, height=4, wrap="word")
        else:
            field = ttk.Entry(parent)
        field.pack(fill="x")
        return field

    @staticmethod
    def _value(widget) -> str:
        return widget.get("1.0", "end").strip() if isinstance(widget, tk.Text) else widget.get().strip()

    def save_input(self) -> None:
        evaluator = self.input_evaluator.get()
        try:
            record_id = self.trial.record_input(EvaluatorInput(
                evaluator, self._value(self.criterion), self._value(self.observation),
                tuple(line.strip() for line in self._value(self.evidence).splitlines() if line.strip()),
                self._value(self.tentative),
            ))
        except TrialBoundaryError as exc:
            messagebox.showwarning("入力を確認してください", str(exc))
            return
        self.records_by_evaluator[evaluator].append((record_id, self._value(self.criterion)))
        self.input_status.configure(text=f"保存しました。記録は {evaluator} だけが共有できます。")
        for field in (self.criterion, self.observation, self.evidence, self.tentative):
            if isinstance(field, tk.Text):
                field.delete("1.0", "end")
            else:
                field.delete(0, "end")
        self._refresh_share_choices()

    def _build_compare(self) -> None:
        ttk.Label(self.compare_tab, text="本人が保存した記録だけを、合議のために共有できます。").pack(anchor="w")
        self.share_evaluator = ttk.Combobox(self.compare_tab, values=EVALUATORS, state="readonly")
        self.share_evaluator.set(EVALUATORS[0])
        self.share_evaluator.pack(fill="x", pady=5)
        self.share_evaluator.bind("<<ComboboxSelected>>", lambda _event: self._refresh_share_choices())
        self.share_choice = ttk.Combobox(self.compare_tab, state="readonly")
        self.share_choice.pack(fill="x", pady=5)
        ttk.Button(self.compare_tab, text="選んだ記録を合議用に共有", command=self.share_input).pack(anchor="e", pady=5)
        ttk.Button(self.compare_tab, text="共有済みの見解を比較", command=self.show_comparison).pack(anchor="e", pady=5)
        self.comparison_text = self._text(self.compare_tab, height=17)
        self.comparison_text.configure(state="disabled")

    def _refresh_share_choices(self) -> None:
        evaluator = self.share_evaluator.get()
        choices = [f"{record_id} | {criterion}" for record_id, criterion in self.records_by_evaluator[evaluator]]
        self.share_choice["values"] = choices
        self.share_choice.set(choices[0] if choices else "")

    def share_input(self) -> None:
        selected = self.share_choice.get()
        if not selected:
            messagebox.showwarning("共有する記録がありません", "先に同じ評価者の記録を保存してください。")
            return
        try:
            self.trial.share_for_consensus(selected.split(" | ", 1)[0], self.share_evaluator.get())
        except TrialBoundaryError as exc:
            messagebox.showwarning("共有できません", str(exc))
            return
        messagebox.showinfo("共有しました", "共有済みの記録だけが比較画面に表示されます。")
        self.show_comparison()

    def show_comparison(self) -> None:
        comparison = self.trial.compare_views()
        lines = ["比較結果（自動の採点・順位付け・結論は行いません）", ""]
        for view in comparison["views"]:
            lines.extend((
                f"【{view['evaluator_id']}】 {view['criterion']}",
                f"観察: {view['observation']}",
                f"根拠: {' / '.join(view['evidence'])}",
                f"暫定見解: {view['tentative_view']}", "",
            ))
        lines.append("共通する根拠: " + (" / ".join(comparison["shared_evidence"]) or "なし"))
        lines.append("異なる根拠: " + (" / ".join(comparison["divergent_evidence"]) or "なし"))
        self._replace_text(self.comparison_text, "\n".join(lines))

    def _build_consensus(self) -> None:
        self.consensus_evaluator = ttk.Combobox(self.consensus_tab, values=EVALUATORS, state="readonly")
        self.consensus_evaluator.set(EVALUATORS[0])
        ttk.Label(self.consensus_tab, text="合議メモを確認する評価者").pack(anchor="w")
        self.consensus_evaluator.pack(fill="x")
        self.consensus_note = self._entry(self.consensus_tab, "人間が確認した合議メモ", multiline=True)
        self.unresolved = self._entry(self.consensus_tab, "未解決事項（複数の場合は改行で区切る）", multiline=True)
        self.human_confirmed = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.consensus_tab, text="人間の評価者として、この合議メモを確認した", variable=self.human_confirmed).pack(anchor="w", pady=8)
        ttk.Button(self.consensus_tab, text="合議メモを記録して報告書草案を見る", command=self.save_consensus).pack(anchor="e")
        self.report_text = self._text(self.consensus_tab, height=12)
        self.report_text.configure(state="disabled")

    def save_consensus(self) -> None:
        try:
            self.trial.record_human_consensus(ConsensusRecord(
                self.consensus_evaluator.get(), self._value(self.consensus_note),
                tuple(line.strip() for line in self._value(self.unresolved).splitlines() if line.strip()),
                self.human_confirmed.get(),
            ))
        except TrialBoundaryError as exc:
            messagebox.showwarning("合議メモを確認してください", str(exc))
            return
        report = self.trial.draft_report()
        self._replace_text(self.report_text, json.dumps(report, ensure_ascii=False, indent=2))

    def _build_feedback(self) -> None:
        self.feedback_evaluator = ttk.Combobox(self.feedback_tab, values=EVALUATORS, state="readonly")
        self.feedback_evaluator.set(EVALUATORS[0])
        ttk.Label(self.feedback_tab, text="試用者").pack(anchor="w")
        self.feedback_evaluator.pack(fill="x")
        ttk.Label(self.feedback_tab, text="使いやすさ（1=使いにくい、5=使いやすい）").pack(anchor="w", pady=(8, 0))
        self.ease = ttk.Spinbox(self.feedback_tab, from_=1, to=5, width=8)
        self.ease.set("3")
        self.ease.pack(anchor="w")
        self.helpful = self._entry(self.feedback_tab, "役立った箇所", multiline=True)
        self.problems = self._entry(self.feedback_tab, "分かりにくかった・不要だった箇所", multiline=True)
        self.would_use = self._entry(self.feedback_tab, "実務で使うなら必要な条件", multiline=True)
        ttk.Button(self.feedback_tab, text="試用の感想を記録", command=self.save_feedback).pack(anchor="e", pady=8)
        self.feedback_status = ttk.Label(self.feedback_tab, text="")
        self.feedback_status.pack(anchor="w")

    def save_feedback(self) -> None:
        try:
            self.trial.submit_feedback(TrialFeedback(
                self.feedback_evaluator.get(), int(self.ease.get()), self._value(self.helpful),
                self._value(self.problems), self._value(self.would_use),
            ))
        except (TrialBoundaryError, ValueError) as exc:
            messagebox.showwarning("感想を確認してください", str(exc))
            return
        self.feedback_status.configure(text="記録しました。この内容もアプリを閉じると消えます。")

    @staticmethod
    def _replace_text(widget: tk.Text, value: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", value)
        widget.configure(state="disabled")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-guide", action="store_true", help="GUIを開かず試用手順を表示する")
    args = parser.parse_args()
    if args.print_guide:
        print(json.dumps(new_trial().manual_guided_trial(), ensure_ascii=False, indent=2))
        return
    root = tk.Tk()
    TrialDesktopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
