# Anthropic edition development

- Preserve the migrated 189 workflow IDs, 16 specialist agents, iOS/Android parity, resources, templates and original branding.
- The old repository remains the upstream; never modify it as part of this edition.
- Installed content is contained in plugins/. Publisher tooling, tests and receipts stay outside those roots.
- Core must not read installer credentials or declare startup hooks, MCP servers or dependencies. Authenticated research uses the optional declared integration and explicit sensitive userConfig.
- Before publication, run regression tests, release validation, full public audit, official strict manifests and real Claude host discovery. Preserve source and directory states separately.
- Do not send support messages or accept new legal agreements without the owner's authorization.
