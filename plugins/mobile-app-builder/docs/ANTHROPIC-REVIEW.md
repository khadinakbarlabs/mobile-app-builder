# Directory review boundary

The core package has 30 entry skills, eight lead agents, eight commands and eight departments. All 190 detailed workflow guides and 16 original role cards remain readable as references. It ships on-demand, readable JavaScript helpers; the PNG brand assets live at the repository root and the approved icon is stored in the directory listing. There are no startup hooks, declared MCP servers, dependency installs, binary executables or automatic paid research in core.

## Credential warning

The directory scan of v2.3.0 reported `MCP_FORWARDS_CREDENTIAL_ENV` against `.claude-plugin/plugin.json`, without identifying a specific credential reader or outbound transfer in the core. The core manifest has no `mcpServers`, `userConfig`, `hooks` or `dependencies`; core JavaScript helpers do not read environment credentials or contact a remote service. The package validator rejects credential-shaped files, common secret patterns, private build-environment examples, environment reads and common network/subprocess calls in core helpers. A separately installed research integration has its own manifest and declared HTTPS connection with a required sensitive `${user_config.apify_token}` value; it is not included in the core directory submission.

The guides can help a user build an app with authentication, paid services, deployment or research in that user's own environment. Those consuming-app operations are separate from installation and must follow the user's permissions and actual project scope. The [technical data-handling page](CLI-DATA-HANDLING.md) identifies destinations for such optional work. This explanation documents the boundary; it does not claim the automated warning has cleared or preempt a reviewer finding. If the reviewer identifies a concrete file or execution path, fix and revalidate that path.

## Listing and image notes

The `icon`, `documentationUrl`, `supportUrl`, `privacyPolicyUrl` and `termsOfServiceUrl` fields are [documented directory listing fields](https://code.claude.com/docs/en/plugins-reference), but the v2.3.0 scan reported them as unrecognized or cross-tool. The submitted directory listing had already imported the links, and its icon was replaced with the v9 image in the directory editor. The listing editor says newer versions do not update those imported details. Version 2.3.2 therefore omits these five fields from the runtime manifest while retaining the linked documents in the package and the artwork in the repository. The v2.3.1 scan additionally named the v9 PNG as a credential finding, so v2.3.2 keeps both image files outside the installed root. Confirm the listing still shows the links and v9 icon after the new scan; re-add the fields if a future fresh submission requires manifest-based import.

Local validation and a completed security scan are separate from a reviewer decision and a live listing. Read the exact version's directory status before claiming publication.
