# Technical CLI and data handling

This page documents optional development-tool behavior for reviewers and people configuring the backend. Service names here identify real data destinations; they are not product branding. No remote service, credential reader or startup hook is declared by the core plugin. Its on-demand local helpers browse prepared metadata, print plans, inspect a bounded set of selected app manifests or turn a supplied JSON report into an offline HTML file. They do not read environment files, installer credentials or remote services. The workflows can guide separately authorized operations in a consuming project.

## Research

Core research uses public sources, user-provided exports, or an independently installed research connection that declares https://mcp.apify.com and explicit sensitive user configuration in its own manifest. It is not installed by core. The owner-operated backend CLI procedure remains in the source repository outside the installed core package. Research may contain public personal data such as names and professional profiles; results can be written to the user's chosen local research folder. Scope, lawful data sources, collection limits and run budget remain explicit. Never borrow an installer's ambient credentials or print a token.

## Development and release

When selected by the user, authenticated build and release CLIs can upload app source, configuration and assets to https://api.expo.dev and related https://expo.dev build services. Store workflows can upload builds, screenshots, metadata and account-authorized release information to Apple App Store Connect, including https://api.appstoreconnect.apple.com, or Google Play, including https://androidpublisher.googleapis.com. Repository workflows can push user-authorized project files to https://github.com. These are consuming-project actions, not plugin installation behavior. Use the owner's approved tool account and exact project scope.

## Project integrations

A consuming app can use its own selected authentication, database, analytics, payments, AI or marketing APIs. No such account, endpoint or SDK is silently provisioned by this plugin. Inspect the actual app configuration and current official documentation, identify each destination and the data it will receive, and establish the user's authorization before a network operation. Do not expose server keys in browser/mobile bundles. Service data retention and deletion are controlled by the selected service and the consuming app, not a plugin-owned policy.

## Storage and disclosure

Host-authorized file tools may read project or user-supplied data and save research summaries and artifacts in the user's workspace. This may include personal data. Minimize collection, redact unnecessary identifiers, avoid public logs and repositories, and keep raw research ignored by source control. The plugin publisher operates no receiver, telemetry collector or research datastore and retains no copy. Configuring an account does not authorize outreach, paid runs, deployment or store publication. Report actual source uploads and network destinations with the work performed.

The project snapshot helper reads only `package.json` and `app.json` contents plus the existence of a small set of platform and instruction files, and returns recognized framework/check names without echoing configuration values. The report renderer reads a user-selected JSON report and writes a self-contained local HTML file to a user-selected path; it does not open or upload that file. Review report inputs for private information before creating or sharing output. A schedule is never installed with the plugin; a user-owned host routine has its own repository, connector and access scope.
