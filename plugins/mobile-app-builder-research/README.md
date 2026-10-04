# Mobile App Builder Research

An optional research connection for Mobile App Builder Agency. The full agency works without this package. Install this integration only when you want the assistant to collect live evidence using an Apify account you explicitly choose to connect. Planning, public-source analysis and user-provided exports remain available without it.

The plugin connects to Apify's documented HTTPS MCP endpoint. The host asks you for an Apify API token in a sensitive required userConfig field and substitutes it into the declared Authorization header. It never reads an existing environment token or CLI credential file, puts the token in a URL or argument, or exposes it to skill text. The manifest and MCP configuration declare the complete connection; there is no startup script, local server, package launcher, automatic dependency install or additional destination.

Selected tools inspect public Actors and their schemas, start an explicitly authorized run, inspect its status, retrieve datasets and summary records, and stop a run. Starting Actors can incur charges. Establish the exact Actor, permitted data, run limits and budget before execution. A configured account alone never authorizes spending or accessing unrelated storage. Some tools added by the provider support run readback; inspect actual available tools after connection.

The [connection workflow](skills/research-connection/SKILL.md) describes setup, provenance and budget boundaries. The [Actor catalog](skills/research-connection/references/actor-catalog.json) preserves the previous real public portfolio routes; snapshots are not proof of current schemas or prices. The [registry template](skills/research-connection/references/actor-registry.json) starts disabled and needs an explicit project selection.

Install `mobile-app-builder-research@khadin-mobile-agency` from the `khadinakbarlabs/mobile-app-builder-agency` marketplace and configure it through the host's plugin configuration. Do not paste a token into chat or edit a public file to set it. If your host cannot collect sensitive plugin configuration, use its supported Apify connector and leave this package disabled. Actual authenticated Actor behavior is not verified by manifest validation; test it within an approved budget before relying on results.

[Privacy](PRIVACY.md) · [Terms](TERMS.md) · [Support](SUPPORT.md) · [Security](SECURITY.md) · [License](LICENSE)
