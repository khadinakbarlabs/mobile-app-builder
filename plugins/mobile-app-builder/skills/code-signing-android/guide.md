---
name: "code-signing-android"
description: "Prepare Android upload signing, Play App Signing and public certificate fingerprints without reading private keystores. Use for signing failures, Firebase fingerprints or upload-key recovery."
---

# Prepare Android signing

Keep the upload key and Play signing key distinct: the owner-controlled upload key signs an AAB before upload; Google Play's app-signing key signs delivered APKs. Compare the intended app/package and public certificate fingerprints before changing configuration.

## Owner-managed credentials

Core does not open a private keystore, retrieve its password, generate secret-file commands, or upload signing material. The owner manages signing in their approved service using [Expo managed credentials](https://docs.expo.dev/app-signing/managed-credentials/) and [Android Play App Signing](https://developer.android.com/studio/publish/app-signing). Reuse verified public information and a redacted setup confirmation. A configured account never authorizes a new signing change by itself.

## Public fingerprint checks

Obtain SHA-1/SHA-256 values from the app's public certificate details in Play Console's App integrity view or the owner's signing service. Compare the upload, debug and delivered-app fingerprints explicitly; they can differ. For Firebase/Google Sign-In, register only the fingerprints appropriate to the selected app and build. Do not open the underlying keystore to get them.

## Recovery

| Symptom | Next action |
| --- | --- |
| Google Sign-In developer error | Compare the selected app's package, OAuth client and public certificate fingerprints. |
| Upload key mismatch | Reconcile the rejected build and approved upload certificate; owner uses Play's supported reset route if necessary. |
| Lost upload key | Owner checks Play App Signing's upload-key reset process and affected app before making a change. |
| Unknown upload outcome | Read back the specific build/track outcome before uploading again. |

Implement public configuration fixes locally, run affected tests, and report signing/device/store evidence separately. Never call a configuration review a signed production build.

## Pair with
- `set-up-play-app-signing`
- `add-google-signin-credential-manager`
