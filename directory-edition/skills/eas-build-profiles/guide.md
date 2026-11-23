---
name: "eas-build-profiles"
description: "Configure EAS build profiles (development, preview, production) with environment variables and resource classes. Use when the user says 'EAS build profiles', 'build configurations', 'env vars EAS'."
---

# EAS Build Profiles

Three default profiles + how to extend them.

## Credential and external action gate

Editing a local profile is safe. Account configuration and cloud builds belong to the owner's delivery environment and may incur cost. Reuse valid authorization for the exact EAS account, project, environment, variable classification and action; obtain only missing decisions. Core does not read installer credentials or private signing files. Have the owner configure private values in the provider interface. Never place a server secret in an `EXPO_PUBLIC_*` variable or commit it to `eas.json`.

## Default 3 profiles
- **development** — `developmentClient: true`, `distribution: internal`. Dev tools enabled. Install dev client on physical iPhone.
- **preview** — `distribution: internal`. Production-style binary for internal QA. Skips TestFlight processing wait.
- **production** — store-bound. No dev client, release config, signed with distribution cert.

## Extending base profiles
```json
{
  "build": {
    "base": {
      "node": "20.19.0",
      "ios": { "resourceClass": "m-medium" },
      "env": { "EXPO_PUBLIC_API_URL": "https://api.example.com" }
    },
    "development": {
      "extends": "base",
      "developmentClient": true,
      "distribution": "internal",
      "channel": "development",
      "ios": { "simulator": true },
      "env": {
        "EXPO_PUBLIC_API_URL": "http://localhost:3000",
        "APP_VARIANT": "development"
      }
    }
  }
}
```

## Resource classes (iOS)
- `m-medium` — default, ~8 min average build
- `m-large` — paid tier, faster, for large apps
- Use `m-large` only if `m-medium` is bottlenecking your dev cycle

## Environment variables — single source of truth
Use **EAS Environment Variables** in the owner-managed web dashboard, scoped to development/preview/production. Prepare the variable name, classification and consuming build environment locally; the owner enters private values directly in the provider interface. Keep non-sensitive public application configuration in the local profile when appropriate.

Three visibility levels:
- **Plaintext** — visible in UI/logs
- **Sensitive** — hidden in UI, readable in build
- **Secret** — only readable inside build job

## Build cache
`eas build --clear-cache` invalidates dependency cache. Use it only after approval for the associated build; cache duration and cost vary by plan and project.

## Reference
`references/02-eas-pipeline.md`
