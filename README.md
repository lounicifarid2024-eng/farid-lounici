# IntelliFamilia — OpenAI Build Week

IntelliFamilia is a privacy-first family coordination demonstration. It turns a
plain-language request into an editable weekly proposal, requires a person to
confirm it, and lets a family create an editable memory draft before approval.

> The assistant proposes. Your family decides.

## What works

- Synthetic household with parent, child, and senior roles
- Plain-language weekly request transformed into a visible draft
- Edit or reject individual proposed items before confirming the week
- Explicit human confirmation and browser persistence
- Synthetic memory scene, editable note, discard/approve controls, and timeline
- Responsive UI and a visible privacy/limitations panel

No real family data, credentials, location, or background automation are used.
All demonstration data stays in the browser's `localStorage`.

## Run locally

Prerequisites: Node.js `>=22.13.0`.

```bash
npm install
npm run dev
```

Then open the local URL printed by the development server.

## Verify

```bash
npm run lint
npm test
```

`npm test` performs a production build, validates the deployable artifact, and
checks the rendered application metadata.

The three core journeys were also tested manually in a browser on July 21,
2026, including edit, reject, confirm, approve, refresh, and persistence.

## Architecture

- React 19 single-page experience
- Next-compatible routing through Vinext/Vite
- Client-side state with `localStorage` persistence
- Deterministic proposal generation for a safe, repeatable judging demo
- No database, authentication, external API, or secret required

See [ARCHITECTURE.md](ARCHITECTURE.md) for the flow and limitations.

## Build Week work

The IntelliFamilia concept and an earlier prototype existed before Build Week.
This focused web implementation was created during Build Week as the judging
demo: it adds the complete human-in-the-loop weekly flow, editable memory flow,
browser persistence, responsive presentation, validation, and deployment
packaging. See [BUILD_WEEK_DELTA.md](BUILD_WEEK_DELTA.md) for the baseline/new-work
boundary.

Codex with GPT-5.6 was used to recover the submission plan, reduce scope to a
demonstrable core, implement the interface and state transitions, run automated
checks, and perform interaction QA. GPT-5.6 is part of the development process,
not a runtime integration: the deployed judging demo deliberately makes no live
model or external API call.

## Limitations

- Demonstration only; not medical, legal, emergency, or care advice
- Synthetic data only
- Single-browser persistence; no multi-user sync
- Proposals are deterministic examples, not live model output
- No notifications or autonomous actions

## Submission category

Apps for Your Life.
