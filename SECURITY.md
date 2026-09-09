# Security Policy — Binôme Intelligent Profile

## Scope

This repository contains a public, self-documented technical profile and a governance validator. It is not an identity-proofing service, certification authority, compliance certification, or professional credential issuer.

## Security principles

- No secrets, API keys, passwords, client data, or confidential material may be committed.
- Sensitive actions remain human-gated.
- Governance is deny-by-default.
- CI has read-only repository permissions.
- The validator uses only the Python standard library at runtime.
- External credentials must be independently verifiable before being represented as credentials.

## Human validation gates

The following categories require explicit human approval before execution in any implementation derived from this profile:

- publication;
- payment;
- contract or signature;
- deletion;
- confidential data release;
- irreversible change.

## Claims discipline

The repository must not claim that the profile is officially certified, scientifically proven, guaranteed compliant, guaranteed performant, or fully autonomous without external evidence supporting the exact claim.

## Reporting

If a security issue is found, open a GitHub issue without including secrets or confidential data. For vulnerabilities involving private credentials, revoke/rotate the affected credential first and avoid publishing it in an issue.
