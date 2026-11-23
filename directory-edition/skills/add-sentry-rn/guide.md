---
name: "add-sentry-rn"
description: "Add Sentry crash reporting and error monitoring to a React Native + Expo app, including source map upload and release tracking. Use when the user says 'add sentry', 'crash reporting', 'error monitoring', 'sentry expo', 'rn crash tracking'."
---

# Add Sentry to React Native + Expo

Crash reporting + error tracking + performance monitoring. Evaluate it against the app's privacy, cost, and observability needs.

## Privacy, credential, and external action gate

Creating a Sentry project, running its wizard, uploading source maps, or storing an auth token changes external services and may expose app metadata. Obtain owner approval for the Sentry organization/project and data-retention settings first. Never put a DSN, auth token, or source-map credential in this plugin, a public repository, a prompt, or logs.

## Why Sentry over alternatives
- Best RN integration (official SDK, source map upload built in)
- Free tier: 5k errors/mo, generous for indie
- Source maps for readable stack traces (vs minified gibberish)
- Replay (see exact UI state at crash)
- Performance traces

## Install (Expo)

```bash
npm exec --no -- expo install @sentry/react-native
npx @sentry/wizard@8.0.0 -i reactNative
# Wizard prompts for Sentry org + project, configures everything
```

This adds:
- `@sentry/react-native` to deps
- `metro.config.js` source map config
- iOS native config to `ios/Podfile`
- Sentry init code to `App.tsx` or `_layout.tsx`

## Basic init (app/_layout.tsx for Expo Router)

```ts
import * as Sentry from '@sentry/react-native';

Sentry.init({
  dsn: 'https://your-dsn@sentry.io/project',

  // Send errors only in production by default
  enabled: !__DEV__,

  // Performance: 10% sampling for prod
  tracesSampleRate: __DEV__ ? 1.0 : 0.1,

  // Replay: 100% of sessions with errors, 10% otherwise
  replaysOnErrorSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,

  // Track release for source map matching
  release: `com.yourapp@${Constants.expoConfig?.version}`,
  dist: Constants.expoConfig?.ios?.buildNumber,

  integrations: [
    Sentry.mobileReplayIntegration(),
  ],
});

export default Sentry.wrap(RootLayout);
```

## EAS Build integration

In the consuming app's `eas.json`, select the build environment:

```json
{
  "build": {
    "production": {
      "environment": "production"
    }
  }
}
```

The app owner adds the Sentry upload secret to that project's production EAS environment with sensitive visibility, or to the selected CI secret store, through the Expo or CI dashboard, following [Expo's Sentry guide](https://docs.expo.dev/guides/using-sentry/#usage-with-eas-build). A string beginning with `@` in `eas.json` is not a secret lookup. The assistant never reads, checks, copies or forwards that secret. Authentication and source-map upload belong to the owner's approved build environment.

Review the wizard's generated changes before a build. After an authorized build, verify the source-map upload and a sanitized test error against the exact release. Environment selection alone does not prove that upload succeeded.

## Manual error capture

```ts
try {
  await riskyOperation();
} catch (e) {
  Sentry.captureException(e, {
    tags: { feature: 'paywall' },
    extra: { userId: user.id, action: 'subscribe' },
  });
}
```

## User context (privacy-aware)

```ts
// On login
Sentry.setUser({
  id: user.id, // hashed/anonymized
  // Don't send email or PII unless you have privacy disclosure
});

// On logout
Sentry.setUser(null);
```

## Performance traces (key flows)

```ts
const transaction = Sentry.startTransaction({ name: 'paywall_purchase_flow' });

// ... do work ...

transaction.finish();
```

Sentry shows P50/P95 timing, breakdowns by step.

## Replay (record session leading to error)

Auto-enabled with `replaysOnErrorSampleRate`. Privacy: by default Sentry masks all text/inputs. To unmask non-sensitive UI:

```tsx
<View dataSet={{ sentryUnmask: true }}>
  <Text>This is OK to record</Text>
</View>
```

## Privacy / disclosure

- Add Sentry to your Privacy Manifest (`privacy-manifest-rn`)
- Mention "we use Sentry for crash reporting" in privacy policy
- Sentry is GDPR-compliant; sign their DPA via dashboard

## Common gotchas

- Source maps not uploading? Ask the app owner to confirm the Sentry upload secret exists in the EAS environment dashboard
- Errors show as "minified.js:1" in production = source map upload failed
- Sentry kills cold start by 50-100ms; use `enableTracing: false` if perf-critical
- Init MUST be the first thing in your entry file or you'll miss early errors

## Pair with
- `add-posthog-rn` for product analytics (different concern, complementary)
- `privacy-manifest-rn` to disclose Sentry properly
- `versioning-fingerprint` so source maps match release versions
