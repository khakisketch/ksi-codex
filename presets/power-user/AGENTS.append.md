## KSI Codex Power User Preset

Power-user mode is for a personal machine where the user wants high-autonomy local development and browser verification.

- Default to executing local/dev tasks instead of asking for step-by-step permission.
- When safe, inspect, edit, run project commands, start dev servers, launch Chromium, use Playwright, capture screenshots, and verify behavior.
- Ask only blocking questions. Prefer brief assumptions plus action.
- Use Chromium + Playwright as the default browser automation path.
- Use visible persistent Chromium profiles for login, MFA, OAuth, cloud consoles, billing consoles, and admin screens.
- Let the user type credentials, OTPs, recovery codes, secrets, and payment details directly in the visible browser.
- Continue automation only after login and only on non-secret UI state.
- Stop before production writes, billable cloud creation/deletion, destructive operations, irreversible external changes, and git commit/push/tag/release unless explicitly requested.
