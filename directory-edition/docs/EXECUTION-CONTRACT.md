# Manual inspection receipt

This directory edition contains no helper programs. When a task starts from an existing repository, the active agent inspects a small, fixed set of public project markers with its ordinary file tools (Read, Glob, `ls`) and writes a short receipt. The receipt is a starting clue. It does not establish a working app, an available toolchain or a device test.

## What to inspect

Look only at the project root the user selected. Check each marker below for existence; read a file's contents only where the table says so.

| Marker | Action | What it tells you |
| --- | --- | --- |
| `package.json` | Read (skip it and say so if it is larger than about 128 KiB) | Dependency **names** and script **names** only |
| `app.json`, `app.config.*` | Read `app.json`; note `app.config.*` exists | An `expo` key means Expo |
| `pubspec.yaml` | Exists | Flutter |
| `ios/`, `android/` | Exists (directory) | Native project folders |
| `build.gradle`, `build.gradle.kts`, `settings.gradle`, `settings.gradle.kts` | Exists | Android / Gradle project |
| `next.config.*`, `vite.config.*`, `angular.json`, `svelte.config.*` | Exists | Web framework |
| `AGENTS.md`, `CLAUDE.md` | Exists (read later if relevant) | Project instructions to follow |

Inspection rules:

- Never open `.env*`, keystores, `*.p8`, `*.p12`, `*.jks`, `*.keystore`, `*.mobileprovision`, `google-services.json` credential values, `GoogleService-Info.plist` secrets, service-account JSON or any file whose name suggests credentials.
- Do not echo script bodies, arbitrary manifest fields or dependency versions you do not need. List dependency names only.
- If a marker is a symbolic link, do not follow it. Record it as "symlink, needs review" and ask the user which target is intended.
- Execute no project code and contact no service during inspection.

## How to infer the app shape

| Evidence | Framework |
| --- | --- |
| `expo` dependency, or an `expo` key in `app.json` | Expo |
| `react-native` dependency without Expo | React Native |
| `pubspec.yaml` | Flutter |
| `next` dependency | Next.js |
| `vite` dependency | Vite |
| `@angular/core` dependency | Angular |
| `@sveltejs/kit` dependency | SvelteKit |
| Gradle file, and none of Expo / React Native / Flutter | Native Android |
| `ios/` folder, and none of Expo / React Native / Flutter | Native iOS |

| Platform | Evidence |
| --- | --- |
| iOS | `ios/` folder, Expo, React Native or Flutter |
| Android | `android/` folder, a Gradle file, Expo, React Native or Flutter |
| Web | `react-native-web` dependency, a web framework above, or a `web` script name |

Stage is **existing-app** when any marker was found, otherwise **idea-or-unknown**. Available checks are the script names `lint`, `test`, `typecheck` and `check` when present; a script name is not proof the check is safe or installed.

## Receipt fields

Write the receipt in the chat and, when the user keeps one, in the project context card ([template](../templates/project-context.md)).

| Field | Meaning |
| --- | --- |
| Task ID | A short lowercase identifier (at most 80 characters) the user supplied, or one you choose; reuse it when continuing the task |
| Observed at | Date and time of the inspection |
| Sources read | The markers actually found and read |
| Stage, frameworks, platforms | Inferred shape; verify against actual code before acting |
| Route | Entry skill chosen from the routing table in [the intelligent workflow](INTELLIGENT-WORKFLOW.md), and whether it came from an explicit request or a keyword hint |
| Verification | Always `manifest-only`: no checks, build, device or external action performed |
| Unknowns | Missing evidence, skipped oversized files, symlinks needing review |
| Next action | One action to carry into the project's checkpoint |

## When inspection is blocked

| Situation | Next action |
| --- | --- |
| Project path not found | Locate the existing app; do not scaffold a replacement |
| Root is not a regular directory, or is a symlink | Ask the user to confirm the intended directory |
| Manifest is not valid JSON | Report it; repair only with permission and without discarding unrelated work |
| Manifest is very large | Inspect the needed parts manually and say so |
| Permission denied | Use an authorized readable project |

Inspection owns no authenticated or external operation. When an authorized service is used later, record authentication failures, partial uploads and unknown outcomes separately. Never convert an external timeout into a success or repeat the action before reconciling its state.
