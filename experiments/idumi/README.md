# IDUMI β0.3 — AI Chat Launcher (experimental)

Standalone browser-only application: open index.html with a browser, or serve it as a static file. This does **not** publish to an existing Sites project.

## Primary flow

1. Configure **1–7 anonymous speakers**, **1–10 replies per generation**, closeness and language style.
2. Fetch selected publicly accessible Protocol texts from GitHub's Contents API. The browser captures the blob SHA and attaches fetched text to the generated prompt. If fetch fails, the prompt says **not retrieved**.
3. Copy the prompt to a user's **own AI Chat**. No model or paid API is called by this app. This is a user-paste process, not a native ChatGPT/Copilot connector.
4. Paste numbered AI responses into the app to validate sequential numbers and append the output. The **1000-reply cap is per thread, not per generation**.
5. Export a JSON-compatible YAML 1.2 candidate carrying posts, settings, references, personal memo and unresolved questions. Import in the same app or create another thread; previous full history should be exported before transition.

## Important boundaries

- The copied one-line Protocol is an instruction; its semantic fidelity to Shirakami v3.2 has **not** been independently verified.
- Referencing OPPAI_Schema_v0.1.md is **not executing OPPAI Runtime**; the protocol list and GitHub blob SHA are displayed as retrieved data. The Registry is an index, not an authorization.
- The model's behavior on closeness/language sliders requires A/B testing and is not guaranteed.
- The browser stores content in localStorage, possibly including private information. Do not use public/shared computers for sensitive sessions; delete local browser data when needed. Exported files must be safeguarded by the user.
- Generated replies are pasted and unverified, not trusted Evidence or an authenticated Human Gate action.
- This experiment is static; no logins, session synchronization, shared threads, user analytics or backend persistence.
- Earlier β0.3-A sources, existing Sites, Workers, D1, protected branches and model API keys are untouched.
- To deploy for public use, perform browser E2E, accessibility and privacy review, GitHub API rate-limit behavior, and protocol-behavior tests against the target AI Chat.

## Quick manual test

Open index.html in a browser and set speakers=1, replies=1. Check copied instruction for those values. Fetch GitHub text, verify each SHA is shown, test an unreachable API case, paste "1 ：名無しさん：テスト" and verify count 1/1000. Verify duplicate "1" is rejected, next valid "2" increments count, and export/import round-trips. Create the next thread and confirm reply numbering begins at 1 and context memo follows the next prompt.

This is **not** an assertion that the above E2E tests have been performed in a live browser.
