# Mobile App Builder

![Mobile App Builder](https://raw.githubusercontent.com/khadinakbarlabs/mobile-app-builder/main/assets/mobile-app-builder-logo-v9.png)

Research, design, build and grow iOS, Android and web apps with 30 focused skills, 8 specialist leads and 8 commands. All 190 detailed workflows remain as readable references. Start with a new idea, improve an existing app, or request one focused task. The assistant selects relevant procedures and returns concrete work and verification evidence.

## Choose your outcome

- **New app:** research the opportunity, define the first useful feature, and design the mobile and web experience.
- **Existing app:** inspect the actual stack, preserve working features and design, reproduce issues, and verify focused fixes.
- **One task:** improve UI/UX, research competitors or creators, prepare screenshots and metadata, check quality, or improve SEO.

See [Start here](docs/START-HERE.md), [workflow index](agency/INDEX.md), [web development](skills/build-web-app/guide.md), [resources](docs/RESOURCES.md) and [prompt examples](docs/PROMPTS.md). Start with `/mobile-app-builder:new-app` or `/mobile-app-builder:improve-app`; the other commands cover research, design, build, testing, launch and growth.

The [context and reporting workflow](docs/INTELLIGENT-WORKFLOW.md) helps the assistant use your current app state, keep decisions in a reviewable project card and recommend one useful next move. For multi-finding work, the assistant writes a Markdown (or static, script-free HTML) report from evidence you choose to include. [Recurring-work recipes](docs/RECURRING-WORK.md) are available when you choose ongoing checks, and [feedback](docs/FEEDBACK.md) is optional. Installation creates no schedule or publisher telemetry.

## Platforms and workflow

The library covers iOS and Android development, native capabilities, store readiness, responsive web UI, routing, rendering, browser accessibility and SEO. Existing apps retain their actual framework; use that framework's appropriate tools and current documentation. Shared code changes require checks on all affected platforms.

Specialists cover research, strategy, UI/UX, engineering, QA, launch and growth. You do not need to learn role names or run a full process for one result. Research works from public sources or user-provided exports. Optional backend research tooling is configured through the technical integration guide, with explicit scope and an approved budget before paid collection.

## Install

```text
/plugin marketplace add khadinakbarlabs/mobile-app-builder
/plugin install mobile-app-builder@khadin-mobile-builder
```

## Directory edition

This is the text-only build of Mobile App Builder for the Claude plugin directory. It contains only Markdown, JSON, YAML and image files: no scripts, hooks or MCP servers.

**Works the same:** all 30 entry skills, 190 detailed guides, 8 commands, 8 specialist agents, the agency catalog, templates and policies. None of the full edition's helpers were on a required path.

**Less exact than the full edition:**

- Project inspection is a written checklist the assistant follows with ordinary file tools instead of a fixed program. The machine-readable JSON receipt (schema version, run UUID, exit codes, safe error codes) is replaced by a short written receipt, and the 128 KiB manifest cap and symlink refusal are instructions rather than enforced checks.
- Task routing is a written precedence table instead of code, so the first entry guide may occasionally differ in borderline wording.
- Reports are written by the assistant (Markdown by default) rather than rendered by a validator. Field length limits, the secret-pattern block and HTML escaping are instructions the assistant follows, not code-enforced checks, and layout can vary between runs.
- There is no command-line catalog browser; read `agency/INDEX.md` or search `agency/catalog.json` instead. The catalog schema check runs only in the repository's release tooling.
- The Expo scaffold planner is a written checklist with the same name rule and pinned commands.
- Expect a few hundred extra tokens when inspecting a project or writing a report.

Paid research, account calls, builds, uploads and store actions still need the user's explicit confirmation, an approved spending ceiling where costs apply, and a read-back of the run state before any retry; a paid start is never retried automatically.

The full edition, with its optional local helpers, is installable from the [GitHub repository](https://github.com/khadinakbarlabs/mobile-app-builder) using the install lines above.

## Execution and data handling

This directory edition provides readable skills, specialist instructions, resources and written procedures. It bundles no executable code. It has no startup hook, declared remote connector, automatic dependency installation, plugin-owned telemetry or hosted backend. The written procedures never read environment credentials or call remote services on their own. Framework examples and development commands apply to the consuming user's project and authorized development environment.

Two procedures replace the local helpers of the full edition. The [manual inspection checklist](docs/EXECUTION-CONTRACT.md) tells the assistant which public manifests to read, which credential files never to open and how to write a short stack and task-route receipt. The [report procedure](docs/INTELLIGENT-WORKFLOW.md) defines the report content limits, a secret-pattern check, HTML escaping and the no-script rule; [the example](templates/decision-report.json) shows the content shape. Inspect the report before sharing it.

The host controls file, shell and network access. Workflows can guide user-authorized project changes, research, builds and release preparation. Accounts, paid runs, deployment and store operations require the user's actual scope. Never discover credentials in arbitrary files or include them in chat or public outputs. Some workflows send user-authorized project sources, builds, assets or research inputs to services beyond declared connectors and can save personal data in the user workspace. The [technical CLI and data-handling page](https://github.com/khadinakbarlabs/mobile-app-builder/blob/main/docs/CLI-DATA-HANDLING.md) lists those destinations and boundaries. The publisher operates no data receiver or datastore.

Validation, behavioral tests, deployed URLs, device evidence, store acceptance and directory approval are separate checks. A release of this workflow library does not establish those outcomes for a consuming app.

[Privacy](PRIVACY.md) · [Terms](TERMS.md) · [Support](SUPPORT.md) · [Security](SECURITY.md) · [License](LICENSE)
