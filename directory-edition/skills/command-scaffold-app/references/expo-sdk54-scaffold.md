# Expo SDK 54 scaffold plan

A credential-free checklist for starting a new Expo app. It describes local commands for the user's own development environment. Nothing here logs in, creates provider accounts, starts a cloud build or changes a store listing.

## 1. Check the project name

The name must:

- start with a lowercase letter;
- contain only lowercase letters, digits and hyphens;
- be at most 63 characters long.

Examples: `habit-tracker` and `app2` are fine; `HabitTracker`, `2app`, `my_app` and `my app` are not. If the name does not fit, suggest a corrected one and ask the user to confirm it before going on. Prefer single hyphens (no `--`) and no trailing hyphen.

## 2. Local commands

Show these to the user with the confirmed name in place of `<name>`, ask for confirmation, then run them one at a time from the parent folder where the app should be created:

| Step | Command | Purpose |
| --- | --- | --- |
| 1 | `npx create-expo-app@5.0.0 <name> --template expo-template-default@54.0.63 --no-agents-md` | Create the project from the pinned SDK 54 template |
| 2 | `cd <name>` | Enter the new project |
| 3 | `npm exec --no -- expo install --fix` | Align Expo-managed dependencies with SDK 54 |
| 4 | `npx expo-doctor@1.20.4` | Check the project for common configuration problems |
| 5 | `npm exec --no -- expo start` | Start the local development server |

Stop and report if any step fails; do not retry with different versions without telling the user.

## 3. Next steps

- Inspect `package.json` and the app configuration before adding dependencies.
- Use `npm exec --no -- expo install <package>` for SDK-compatible Expo packages.
- Add `AGENTS.md` project guidance after confirming the stack.
- Run lint, type and test checks before any prebuild or EAS work.

## 4. Safety boundary

- This plan creates only a local folder after the user confirms; it does not log in or create accounts.
- Do not put provider credentials, signing files or `.env` values in the project or in chat.
- Ask for a fresh confirmation, with a named target, before prebuild, EAS builds, store uploads or publication.
