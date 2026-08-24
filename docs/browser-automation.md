# Browser Automation

KSI Codex defaults to Chromium + Playwright for browser automation.

## Default Browser

Use Chromium first. Use Firefox only when:

- the user explicitly asks for Firefox
- Chromium is blocked by a browser-specific issue
- the project has an existing Firefox-specific test target

## Standard Flow

1. Launch visible Chromium with a persistent profile.
2. Let the user complete login, MFA, OAuth approval, or console access directly in the browser.
3. Continue automation from the same session after login.
4. Use Playwright for DOM-aware actions, screenshots, console logs, network inspection, and verification.
5. Use visible-window tools only as fallbacks.

Example:

```bash
python3 scripts/browser.py open --profile oracle --url https://cloud.oracle.com/
```

Profiles live under:

```text
$HOME/.cache/ksi-browser/<profile>
```

## Tool Roles

- Playwright: primary DOM-aware automation and verification
- Chromium: default visible browser and automation target
- `wmctrl`: locate and manage visible browser windows
- `xdotool`: focus windows and provide keyboard/click fallback
- ImageMagick `import`/`convert`: targeted screenshots and image conversion
- `xclip`: clipboard handoff for non-secret text

## Secret Safety

Do not ask for, store, paste, or automate entry of:

- passwords
- OTPs
- recovery codes
- API secrets
- private keys
- payment details

The user enters those directly in visible Chromium. Codex resumes only after login and only on non-secret UI state.

## External Console Safety

Stop before billable, destructive, production, or irreversible external actions unless the user explicitly accepts that specific action.

Examples:

- creating or deleting cloud resources
- changing billing settings
- deleting databases or storage buckets
- modifying production environment variables
- rotating production credentials

## Durable Tests

Browser exploration is not a replacement for durable tests. Important recurring UI/runtime issues should become repo-owned Playwright, Cypress, or framework-native tests.
