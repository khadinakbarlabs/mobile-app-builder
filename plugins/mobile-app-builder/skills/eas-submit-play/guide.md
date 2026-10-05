---
name: "eas-submit-play"
description: "Prepare a controlled AAB upload to Google Play Console via EAS Submit. Use when the user asks to submit an Android build to Play."
---

# EAS Submit to Play

Prepare an AAB upload to Play Console. The final upload and any promotion are owner-confirmed external actions.

## External action gate

Core never reads or uploads a local service-account key or borrows an installer login. Prepare the submission only within the owner’s authorized account, app, build, track and release status; execution belongs to their separately configured delivery environment. A draft upload and a production release are separate decisions.

## Prerequisites

1. App created in Play Console; verify the current first-submission requirements for this app
2. Owner-managed service credentials configured in the selected EAS project
3. `eas.json` configured

## Service Account setup

The owner configures the Google service-account key in the EAS dashboard for the selected app, following [Expo's Android submission prerequisites](https://docs.expo.dev/submit/android/). Scope Play permissions to that app and the intended track; do not grant all-app or production-release access for an internal testing upload. Core never opens or uploads the local key file and does not configure a local credential-file path. Record only a redacted setup confirmation and the intended account/app.

## `eas.json` submit section
```json
{
  "submit": {
    "production": {
      "android": {
        "track": "internal",
        "releaseStatus": "draft"
      }
    }
  }
}
```

`track` options: `internal`, `alpha`, `beta`, `production`.
`releaseStatus`: `draft` (review only), `inProgress` (start staged), `completed` (full release).

## Owner-controlled submission

After the exact account, build and track are authorized, the owner or their separately configured delivery integration submits in its approved authenticated environment. The core can prepare this command without executing it using an installer's saved login:
```bash
eas submit --platform android --profile production --id <verified-build-id>
```

Use the recorded build ID. Reconcile an uncertain submission by that build and the target track before another upload. A command plan is not a completed submission.

## Common gotchas
- "Authentication failed" → owner checks the selected dashboard credential, app permissions and API enablement; core does not inspect the key
- "App not found" → verify the package ID, app creation, selected account permissions and current first-submission requirements; do not assume a manual first upload is always required
- "Track not available" → app not yet promoted to that track (rollout from lower track first)
- "Already in review" → inspect the existing review and version status before another submission; do not cancel it automatically

## Track lifecycle
```
Internal (immediate) → Closed (alpha/beta) → Open (testing) → Production
```

Promote between tracks only after a separate owner confirmation of the target track and release status.

## Pair with
- `internal-testing-track`, `closed-testing-track`, `phased-release-play`
