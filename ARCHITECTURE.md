# Architecture

## Product loop

1. A person creates or loads a synthetic household.
2. A person describes the family's week in plain language.
3. IntelliFamilia creates a visible, editable proposal.
4. The person edits or rejects individual items.
5. Nothing is saved as the week until the person explicitly confirms.
6. A person chooses a synthetic memory scene and writes a note.
7. The memory remains an editable draft until it is approved.

## Technical shape

The application is a client-rendered React experience. State is held in React
and mirrored to browser `localStorage` so the confirmed week and approved
memory survive refresh. The safe demo data is deliberately synthetic and all
proposal generation is deterministic, making the judging path repeatable.

No backend, external API, secret, account, GPS, microphone, or background task
is required. That reduces privacy and availability risk for the submission,
while keeping human agency visible in every important state transition.

## Trust boundary

The application can propose and preserve drafts. It cannot make a family
decision, contact a person, change a calendar, or infer health/care needs.
Confirmation and approval are explicit human actions.
