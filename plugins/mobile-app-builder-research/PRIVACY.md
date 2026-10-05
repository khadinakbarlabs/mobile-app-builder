# Privacy policy

Effective date: October 4, 2026

Mobile App Builder Research is an optional Apify MCP connection with a separate public Actor discovery command powered by the installed Apify CLI. The CLI discovery script sends the search topic to Apify in an isolated temporary home, disables CLI telemetry and update checks, and does not inherit ambient account tokens or open the user's CLI login. It does not start an Actor. The user explicitly provides a token for authenticated MCP research through the host's required sensitive plugin configuration. The host stores and substitutes that value under its secure configuration controls. The plugin sends it only as an Authorization header to the declared HTTPS MCP endpoint at mcp.apify.com. It does not read ambient environment tokens, CLI credential stores, keychains or arbitrary files and does not insert a token into chat, a URL, skill text, a shell argument or a plugin-owned log.

Research queries, selected Actor IDs, permitted input, run/status/storage identifiers and requested results use that connection. Apify and the selected Actors may process these inputs and retrieve data from their documented source platforms. Review the exact Actor's schema, rights, privacy practices and pricing before running. Public listings, reviews, ads, search results and professional creator profiles may include personal data; public accessibility alone is not permission for every use.

The plugin has no custom server, account system, database, telemetry collector or cloud storage. It supplies configuration and workflow instructions. The host, Apify, selected Actors and source platforms apply their own access, logging and retention policies. Avoid unnecessary personal data, keep raw exports in the consuming user's controlled research folder, and redact public outputs. The plugin does not impose a provider retention schedule or guarantee deletion from third-party systems.

A configured token does not authorize a paid run, unrelated account access, private scraping, publication or outreach. Limit collection to the user's requested scope and approved budget. Do not submit credentials as Actor input or send them to another endpoint. Remove or reconfigure the plugin in the host to disconnect it; manage exposed credentials through the issuing provider.

See the source repository's support and security process for a redacted defect report. Do not include tokens, raw private data or unredacted request/response logs.
