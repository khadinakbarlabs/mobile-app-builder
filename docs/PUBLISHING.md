# Publisher guide

Run `python3 -m unittest discover -s tests -p 'test_*.py'`, then `python3 tools/release.py`. Source-only dependencies are pinned in requirements-dev.txt. Archives are written to dist/2.1.0, each with a single plugin root and a complete file/hash inventory. They are not placed inside installed folders.

Run the public audit against the repository and both installed roots. Run the supported host CLI version 2.1.287 strict validation against the marketplace and each plugin manifest. Use `node tools/verify-host.mjs plugins/mobile-app-builder` and the optional research folder to compare actual host discovery with the files. Current native skill/agent schema checks are required in addition to manifest checks.

To prepare directory validation, use the public repository with plugin path plugins/mobile-app-builder and tracked branch main. Submit that folder individually after owner review. The optional research folder is a separate plugin and must be validated and behavior-tested independently. Do not select the repository root as the plugin path; that is a marketplace, not a combined installed package.

Do not withdraw the previous submission, accept new legal declarations, configure a secret, or create a replacement directory submission just to run local checks. Owner authorization for a new submission and its declarations remains a distinct external gate. Keep repository, manifest/host checks, live account behavior, directory scan, reviewer clearance and live listing evidence separate.
