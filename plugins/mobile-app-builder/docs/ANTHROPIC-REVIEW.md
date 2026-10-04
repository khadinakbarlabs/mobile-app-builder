# Directory review boundary

The core package has 30 entry skills, eight lead agents, eight commands and eight departments. All 190 detailed workflow guides and 16 original role cards remain readable as references. It ships two PNG brand assets and on-demand, readable JavaScript helpers. There are no startup hooks, declared MCP servers, dependency installs, binary executables or automatic paid research in core.

## Credential warning

The directory scan of v2.3.0 reported `MCP_FORWARDS_CREDENTIAL_ENV` against `.claude-plugin/plugin.json`, without identifying a specific credential reader or outbound transfer in the core. The core manifest has no `mcpServers`, `userConfig`, `hooks` or `dependencies`; core JavaScript helpers do not read environment credentials or contact a remote service. The package validator rejects credential-shaped files, common secret patterns, private build-environment examples, environment reads and common network/subprocess calls in core helpers. A separately installed research integration has its own manifest and declared HTTPS connection with a required sensitive `${user_config.apify_token}` value; it is not included in the core directory submission.

The guides can help a user build an app with authentication, paid services, deployment or research in that user's own environment. Those consuming-app operations are separate from installation and must follow the user's permissions and actual project scope. The [technical data-handling page](CLI-DATA-HANDLING.md) identifies destinations for such optional work. This explanation documents the boundary; it does not claim the automated warning has cleared or preempt a reviewer finding. If the reviewer identifies a concrete file or execution path, fix and revalidate that path.

## Listing and image notes

The manifest's `icon`, `documentationUrl`, `supportUrl`, `privacyPolicyUrl` and `termsOfServiceUrl` are [documented directory listing fields](https://code.claude.com/docs/en/plugins-reference). Claude Code ignores them at load time, while the directory reads them for the listing. Keep them unless a reviewer identifies an actual compatibility issue. The referenced icon and banner are ordinary, decoded PNG artwork. The scanner's “images and fonts passed without a code check” note is informational and does not imply the images execute as code.

Local validation and a completed security scan are separate from a reviewer decision and a live listing. Read the exact version's directory status before claiming publication.
