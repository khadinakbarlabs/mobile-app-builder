---
name: guide-reliability
description: "Fix an existing app's crash, stuck loading state, failed request, runtime error, slow screen or broken behavior. Reproduce the affected journey, preserve its stack and verify a focused repair. Also use for app performance and monitoring work."
---

# Performance, monitoring and reliability

Choose the smallest relevant workflow. Read its detailed guide and references before acting. Separate source-backed observations from hypotheses; check current platform and store documentation when rules may have changed. Preserve the existing app and verify affected behavior.

For a focused defect, inspect the failing source path and existing checks first. Reproduce the failure with the smallest meaningful check, implement the repair, and rerun that check plus any affected existing checks. For a stuck login spinner, cover both rejection and success, settle the loading state on every completed path, and preserve the app's existing error presentation. Use its current framework and session adapter; no account setup is needed for a local mocked failure. Report source checks separately from a simulator or device observation. Use the specialist guides below only when they match the actual cause or requested work.

| Workflow | Platform | Detailed guide |
| --- | --- | --- |
| add-sentry-rn | shared | [Open guide](../add-sentry-rn/guide.md) |
| add-sentry-rn-android | android | [Open guide](../add-sentry-rn-android/guide.md) |
| enable-r8-proguard | android | [Open guide](../enable-r8-proguard/guide.md) |
| handle-anr-android | android | [Open guide](../handle-anr-android/guide.md) |
| optimize-aab-size | android | [Open guide](../optimize-aab-size/guide.md) |
| optimize-bundle-size | ios | [Open guide](../optimize-bundle-size/guide.md) |
