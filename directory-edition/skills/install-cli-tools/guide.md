---
name: "install-cli-tools"
description: "Plan an owner-confirmed iOS and Expo CLI toolchain without exposing account credentials or running remote installer scripts. Use when the user says 'install CLIs', 'install eas cli', 'install fastlane', or 'install ios cli tools'."
---

# Install iOS and Expo CLI Tools

These tools can alter a development machine or open provider login flows. Present the exact selected tools, their source, and their side effects before installing anything. Never pipe a network download into a shell.

## External action gate

Installing tools can change a development machine. Reuse an existing explicit authorization that names the selected tool, installation source and intended action. If those details are missing, prepare the exact installation for review and continue local analysis while waiting for the missing decision. A build or repair request alone does not authorize a global installation.

Account login and signing setup belong to the owner's provider interface or dedicated delivery environment. This core plugin prepares the toolchain and checks public project configuration; it does not retrieve the installer's credentials.

## Common local tools

| Tool | Purpose | Safer installation boundary |
|---|---|---|
| EAS CLI | Expo build and submit tooling | Approved Node package manager |
| Fastlane | Apple automation | Approved system package manager |
| Sentry CLI | Source-map and release operations | Approved system package manager |
| Maestro | Mobile E2E testing | Official package-manager tap or verified release artifact |
| GitHub CLI | Repository operations | Approved system package manager; `gh auth login` needs owner confirmation |

For an explicitly approved macOS/Homebrew setup, install only the tools needed for the current project:

```bash
npm install -g eas-cli
brew install fastlane
brew install getsentry/tools/sentry-cli
brew tap mobile-dev-inc/tap
brew install maestro
brew install gh
```

For a build or upload, prepare the exact project, build identifier, target and verification plan. Continue an already authorized release in the owner-managed delivery environment. Reconcile a timed-out upload before repeating it. Ask only for authorization that is still missing for the particular external action.

## Verify

```bash
eas --version
fastlane --version
sentry-cli --version
maestro --version
gh --version
```

## Credential handling

- Never save Apple `.p8` files, EAS tokens, Sentry tokens, or provider keys in this plugin, a public repository, shell history, or screenshots.
- Have the owner use the provider's login or secret-storage interface. Do not inspect login caches, private signing files or credential stores, and do not ask a user to paste a credential into chat.
- Prefer least-privilege, project-scoped credentials and rotate/revoke them when access changes.
