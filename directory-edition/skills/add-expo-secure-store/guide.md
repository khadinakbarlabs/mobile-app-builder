---
name: "add-expo-secure-store"
description: "Use expo-secure-store for secrets (tokens, API keys) backed by iOS Keychain. Use when the user says 'secure storage', 'Keychain', 'store token', 'API key storage'."
---

# Add Expo Secure Store

Encrypted at-rest storage backed by iOS Keychain. Use for auth tokens, API keys, anything sensitive.

## Install
```bash
npm exec --no -- expo install expo-secure-store
```

## Usage
```ts
import * as SecureStore from 'expo-secure-store';

// Save
await SecureStore.setItemAsync('authToken', token);

// Delete
await SecureStore.deleteItemAsync('authToken');

// With biometric protection (Face ID / Touch ID required to unlock)
await SecureStore.setItemAsync('vaultKey', secret, {
  requireAuthentication: true,
  authenticationPrompt: 'Authenticate to access your vault',
});
```

These are consuming-app examples: values come from that app's explicit sign-in or user input, never from the plugin installer's environment or Keychain. Implement retrieval inside the app's session/storage adapter using [Expo's SecureStore API](https://docs.expo.dev/versions/latest/sdk/securestore/); handle an absent value, canceled authentication, biometric invalidation and sign-out. The assistant must not extract a real stored value to verify this guide. Test the adapter with synthetic app-session fixtures and on the app's intended devices.

## ABSOLUTE NO
- Never store tokens in AsyncStorage or MMKV (no encryption at rest)
- Keep entries small and handle platform storage errors; large encrypted data needs a separately designed storage and key lifecycle.
- Never call from main thread in tight loops (it's async, use it that way)

## Add Face ID permission
```json
{
  "expo": {
    "ios": {
      "infoPlist": {
        "NSFaceIDUsageDescription": "Access your secure vault"
      }
    }
  }
}
```

## Reference
`references/01-expo-sdk-54.md`
