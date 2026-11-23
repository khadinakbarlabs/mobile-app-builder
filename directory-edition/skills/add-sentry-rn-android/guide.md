---
name: "add-sentry-rn-android"
description: "Add Sentry for crash reporting + source map upload on Android. Use when the user says 'sentry android', 'crash reports android'."
---

# Sentry (Android)

Use the shared [Sentry workflow](../add-sentry-rn/guide.md), including its privacy and external-action boundaries. The following notes apply to Android in the consuming app; they do not configure this plugin.

## Install
```bash
npm exec --no -- expo install @sentry/react-native
npx @sentry/wizard@8.0.0 -i reactNative
```

## Source maps in EAS

Select the owner's intended build environment in the consuming app's `eas.json`:

```json
{
  "build": {
    "production": {
      "environment": "production"
    }
  }
}
```

The app owner adds the Sentry upload secret to that production EAS environment with sensitive visibility, or to the approved CI secret store, through the Expo or CI dashboard. A string beginning with `@` in JSON is not a secret lookup. The assistant never reads, checks, copies or forwards that secret. See [Expo's Sentry build guidance](https://docs.expo.dev/guides/using-sentry/#usage-with-eas-build).

With the SDK and build integration configured, an authorized build can upload source maps. Verify the actual upload and release match; do not infer success from a production profile alone.

## Native crashes
Native Android crashes also captured. Set up symbol upload via Sentry Android SDK (auto with wizard).

## Distinguish from Firebase Crashlytics
- Sentry: better dev UX, breadcrumbs, releases. Pay $26+/mo.
- Crashlytics: free, integrated with Google. Use both — different focus.

## Common gotchas
- ProGuard mapping not uploaded → minified stacks; check EAS post-build hook
- Bundle ID mismatch → events drop silently

## Pair with
- iOS plugin's `add-sentry-rn`
- `add-firebase-crashlytics`
