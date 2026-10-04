# Anthropic edition architecture

This is a new Anthropic-specific source repository derived from the owner's Mobile App Builder v1.3.9. Its purpose is to make the installed component boundary and authenticated research data flow explicit. It is not a claim that a new repository bypasses review or guarantees that the previous hold disappears.

## Installed packages

- `plugins/mobile-app-builder-agency`: the complete 189-workflow library, 16 native specialist agents, eight departments, references, templates, original artwork and four readable local helpers. Default native discovery loads `skills/` and `agents/`. Helpers only print a plan or read a prepared local catalog; they do not read credentials, start remote research or run on installation.
- `plugins/mobile-app-builder-research`: an optional Apify connection using a sensitive required `userConfig` value and one declared HTTPS MCP endpoint. It has no shell launcher, environment-derived token, package download or startup hook. Core does not depend on it. Installing core does not install this connection.

All publisher tools, tests, receipts and migration records live outside these two roots. ZIPs contain one selected plugin root; a marketplace manifest at the repository root lists the two independently installable folders. A directory submission names the core folder, not the marketplace repository as a whole.

## Preserve the product

Workflow IDs, role identities, iOS/Android parity, Actor catalog routes, design resources and brand images are migrated from the exact previous native Git commit. Research, UI/UX, design inspiration, engineering, QA, store screenshots and metadata, Apple/Play intelligence, TikTok/Instagram/YouTube creator research, TikTok/Meta/Google ad intelligence and SEO remain available. The research credential route changes, not these capabilities.

## Research execution

An existing connected Apify tool or the optional research plugin handles explicitly authorized runs. The assistant never discovers a token in the installer's environment, CLI store or files. The retained CLI playbook is an owner-operated alternative, with its authorization boundary stated directly. The Actor registry starts disabled; the real public catalog is preserved, and every selected Actor schema, price and permission is rechecked before a run.

The declared token is substituted only into the Apify MCP header. It is never inserted into skill text, command arguments or logs. Actor execution still needs the user's run scope and budget; configuring a token alone does not authorize spending.

## Release evidence

Before publication, validate complete source containment and file sizes, all YAML frontmatter, Markdown links, local module imports, supported media, credential boundaries and every file's hash. Test rejection cases first. Compare migrated file hashes and disclose every changed or relocated file. Run official native manifest and marketplace validators plus actual native host discovery. Produce reproducible archives and verify their content against the inventory.

Manifest checks, host discovery, GitHub publication, live Actor behavior and Anthropic directory approval are separate evidence. The old v1.3.9 remains in review and is not withdrawn. This edition is prepared for owner verification before any new directory submission.
