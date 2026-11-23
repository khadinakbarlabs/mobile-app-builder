---
name: "add-expo-secure-store-keystore"
description: "Add expo-secure-store backed by Android Keystore for storing auth tokens and secrets. Use when the user says 'secure store android', 'keystore android', 'store token secure'."
---

# Add Expo Secure Store (Android Keystore)

Hardware-backed encrypted key-value store. Uses Android Keystore on Android.

## Install
```bash
npm exec --no -- expo install expo-secure-store
```

## Basic use
```tsx
import * as SecureStore from 'expo-secure-store';

export async function saveAppSession(sessionValue: string) {
  await SecureStore.setItemAsync('app-session', sessionValue);
}
export async function clearAppSession() {
  await SecureStore.deleteItemAsync('app-session');
}
```

The value is supplied by the consuming app's sign-in flow. Keep session retrieval in the app's storage adapter following [Expo's documented API](https://docs.expo.dev/versions/latest/sdk/securestore/), with missing-value, invalidation and authentication-cancellation handling. Never inspect the installer's credential store or use a real token in a plugin test. Verify app persistence and sign-out with synthetic fixtures, then on the intended Android build.

## Android-specific options

```tsx
// Require biometric or PIN to access (Android 6+)
await SecureStore.setItemAsync('sensitive', 'value', {
  requireAuthentication: true,
  authenticationPrompt: 'Verify to unlock',
});
```

## What it uses under the hood

- Android: EncryptedSharedPreferences + Android Keystore (hardware-backed on TEE/StrongBox devices)
- Each key encrypted with hardware-derived key
- Android entries do not survive uninstall or app-data clearing; exclude encrypted entries from backups that cannot restore their Keystore key.

## When NOT to use SecureStore

- Large data (use SQLite encrypted instead)
- Frequently-read values (slow ~5-10ms per read)
- Data that should survive uninstall (use cloud sync)

## When to use

- Auth tokens (access, refresh)
- API keys for the user's session
- Encryption keys for local SQLite
- Sensitive user inputs (PIN, recovery phrase)

## Gotcha: rooted devices

SecureStore relies on Android Keystore. On rooted devices, Keystore can be bypassed. For high-value apps, also implement:
- `add-app-attestation` (Play Integrity API)
- Server-side validation

## Pair with
- `add-supabase-auth-android` for token persistence
- Use MMKV (`add-zustand` persistence) for non-sensitive data
