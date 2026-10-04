# Mobile App Builder Agency

![Mobile App Builder](assets/mobile-app-builder-logo-v8.png)

A complete mobile app agency for iOS and Android: 189 reusable workflows and 16 specialist agents organized into eight departments. Start with an idea, improve an existing app, or request one focused research, design, development, QA, launch or growth task. The assistant selects relevant procedures and returns reviewable work, evidence and practical next steps.

## Start with your outcome

- **New app:** “Research this app idea, identify the first useful feature, and prepare a design and implementation plan.”
- **Existing app:** “Inspect my app, reproduce this onboarding issue, fix it and verify the affected behavior.”
- **Focused task:** “Improve my screenshots,” “Research creators for this audience,” or “Review my SEO and App Store positioning.”

See [Start here](docs/START-HERE.md), [department index](agency/INDEX.md), [workflow library](WORKFLOWS.md), [resources](docs/RESOURCES.md) and [prompt examples](docs/PROMPTS.md).

## Agency departments

| Department | Ownership |
| --- | --- |
| Research | Market evidence, Apple/Play intelligence, creators, ads and search |
| Strategy | Product positioning, validation, pricing and first useful feature |
| Design | UI/UX, inspiration, onboarding, paywalls and design handoff |
| Engineering | Architecture, Expo and native capabilities, app features and fixes |
| Quality | Behavior, accessibility, performance, privacy and security |
| Launch | Screenshots, metadata, signing, submission and rollout |
| Growth | Advertising, influencers, organic acquisition, retention and SEO |
| Operations | Scope, handoffs, evidence, blockers and release readiness |

## Research and integrations

Planning and analysis work without a research connection. Use public sources or user-provided research exports. For live Actor collection, use an explicitly connected Apify tool or install the optional Mobile App Builder Research integration from the same marketplace. It prompts for a token through the host's sensitive user configuration and declares exactly where it is sent. This core package does not install that integration or acquire credentials from the user's machine.

The preserved [Actor catalog](skills/apify-mobile-research/references/actor-catalog.json) contains the previous real portfolio routes and dated schema snapshots. Choose an exact Actor from live inspection. Establish scope, permitted data and a budget before collection; a token alone is not permission to spend. The [research workflow](skills/apify-mobile-research/SKILL.md) covers provenance, results, limitations and safe handoffs.

## What the package runs

The host loads skills and native agents from their standard folders. Four readable local helpers can print an Expo plan or browse a prepared catalog when explicitly requested. They do not read environment credentials, call remote services, fetch or run downloaded code, or execute at installation. No startup hook, declared MCP server, automatic dependency installation, telemetry collector or hosted backend is bundled in core. App code examples concern the user's consuming app, not the installer's credentials.

The host controls file, shell and network access. A workflow can guide user-authorized app development, package installation, project APIs, builds and store operations. These can require project accounts and incur costs; actual access needs the existing session scope. Credentials are configured by the owner through the relevant provider or declared integration, never discovered in arbitrary files or printed in chat. Local checks do not prove a device build, working provider account, successful store submission or directory approval.

## Install

In the supported host CLI, add `khadinakbarlabs/mobile-app-builder-agency` as a marketplace, then install `mobile-app-builder-agency@khadin-mobile-agency`. The optional `mobile-app-builder-research@khadin-mobile-agency` is a separate installation. Follow the repository's installation guide for configuration and current surface limitations.

Directory status: this rebuilt edition is prepared for review; it has not been submitted or approved by Anthropic. The previous Mobile App Builder v1.3.9 remains in its existing review. See [distribution notes](docs/DISTRIBUTION.md).

[Privacy](PRIVACY.md) · [Terms](TERMS.md) · [Support](SUPPORT.md) · [Security](SECURITY.md) · [License](LICENSE)
