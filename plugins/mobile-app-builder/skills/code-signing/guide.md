---
name: "code-signing"
description: "Prepare iOS certificates, provisioning profiles, entitlements and owner-managed signing recovery for the selected app. Use for code signing, expired profiles or App Store Connect key setup."
---

# Prepare iOS signing

Inspect public app configuration, target bundle identifiers, capabilities and redacted build errors. Prefer the project's existing signing strategy. Produce a concrete signing checklist and keep local development moving while account setup is pending.

## Owner-managed credentials

Private keys, signing certificates and account sessions stay with the app owner. Core does not read, upload or print local signing material, borrow an installer's account, or populate secret fields. The owner completes credential creation, upload, rotation or revocation in the approved provider interface using [Expo's managed-credentials workflow](https://docs.expo.dev/app-signing/managed-credentials/). A separate explicitly configured integration can perform only its declared, authorized operations.

For App Store Connect, the owner selects the account and a least-privilege role, records non-secret key/issuer identifiers where needed, and stores the private key in their approved signing service. Verify setup from a redacted provider confirmation; never request a private key file or its contents in chat. Do not generate a file-upload command for that key.

## Useful checks without credential access

- Compare target bundle identifiers and entitlements against the intended app and extensions.
- Check that development, preview and production profiles select the intended signing strategy.
- Use public certificate/profile expiry dates and redacted provider error codes supplied by the owner.
- Record the source revision, build identity and account-dependent step separately.

## Recovery

| Symptom | Next action |
| --- | --- |
| Expired profile | Owner checks the affected profile in the signing service and renews it; reconcile the exact build before retrying. |
| No profile for an extension | Compare each target identifier and capability; owner configures the missing target's signing. |
| App Groups or Push mismatch | Fix app entitlements locally, then owner updates the affected profile. Do not revoke shared profiles speculatively. |
| Uncertain build start | Read back the recorded build ID/status through the selected provider before starting another build. |

A public configuration check is not a successful signed build. Finish with the corrected configuration, checks performed, the precise owner step still needed, and the next verification.

## Reference
`references/02-eas-pipeline.md`
