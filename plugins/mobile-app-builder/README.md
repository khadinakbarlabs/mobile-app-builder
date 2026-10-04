# Mobile App Builder

![Mobile App Builder](assets/mobile-app-builder-logo-v8.png)

Research, design, build and grow iOS, Android and web apps with 30 focused skills, 8 specialist leads and 8 commands. All 190 detailed workflows remain as readable references. Start with a new idea, improve an existing app, or request one focused task. The assistant selects relevant procedures and returns concrete work and verification evidence.

## Choose your outcome

- **New app:** research the opportunity, define the first useful feature, and design the mobile and web experience.
- **Existing app:** inspect the actual stack, preserve working features and design, reproduce issues, and verify focused fixes.
- **One task:** improve UI/UX, research competitors or creators, prepare screenshots and metadata, check quality, or improve SEO.

See [Start here](docs/START-HERE.md), [workflow index](agency/INDEX.md), [web development](skills/build-web-app/guide.md), [resources](docs/RESOURCES.md) and [prompt examples](docs/PROMPTS.md). Start with `/mobile-app-builder:new-app` or `/mobile-app-builder:improve-app`; the other commands cover research, design, build, testing, launch and growth.

The [context and reporting workflow](docs/INTELLIGENT-WORKFLOW.md) helps the assistant use your current app state, keep decisions in a reviewable project card and recommend one useful next move. For multi-finding work, it can make a self-contained visual HTML report from evidence you choose to include. [Recurring-work recipes](docs/RECURRING-WORK.md) are available when you choose ongoing checks, and [feedback](docs/FEEDBACK.md) is optional. Installation creates no schedule or publisher telemetry.

## Platforms and workflow

The library covers iOS and Android development, native capabilities, store readiness, responsive web UI, routing, rendering, browser accessibility and SEO. Existing apps retain their actual framework; use that framework's appropriate tools and current documentation. Shared code changes require checks on all affected platforms.

Specialists cover research, strategy, UI/UX, engineering, QA, launch and growth. You do not need to learn role names or run a full process for one result. Research works from public sources or user-provided exports. Optional backend research tooling is configured through the technical integration guide, with explicit scope and an approved budget before paid collection.

## Install

```text
/plugin marketplace add khadinakbarlabs/mobile-app-builder
/plugin install mobile-app-builder@khadin-mobile-builder
```

## Execution and data handling

This core provides readable skills, specialist instructions, resources and six on-demand local helpers. It has no startup hook, declared remote connector, automatic dependency installation, plugin-owned telemetry or hosted backend. The helpers do not read environment credentials or call remote services. Framework examples and development commands apply to the consuming user's project and authorized development environment.

Two additional on-demand local helpers can inspect a bounded set of app manifests and render an offline report. Run `node scripts/inspect-project.mjs /path/to/app --goal "your outcome"` for a small stack snapshot. To render a report, prepare JSON using [the example](templates/decision-report.json) and run `node scripts/render-report.mjs /path/to/report.json --output /path/to/report.html`. Both run only when invoked; inspect the report input before sharing its output.

The host controls file, shell and network access. Workflows can guide user-authorized project changes, research, builds and release preparation. Accounts, paid runs, deployment and store operations require the user's actual scope. Never discover credentials in arbitrary files or include them in chat or public outputs. Some workflows send user-authorized project sources, builds, assets or research inputs to services beyond declared connectors and can save personal data in the user workspace. The [technical CLI and data-handling page](docs/CLI-DATA-HANDLING.md) lists those destinations and boundaries. The publisher operates no data receiver or datastore.

Validation, behavioral tests, deployed URLs, device evidence, store acceptance and directory approval are separate checks. A release of this workflow library does not establish those outcomes for a consuming app.

[Privacy](PRIVACY.md) · [Terms](TERMS.md) · [Support](SUPPORT.md) · [Security](SECURITY.md) · [License](LICENSE)
