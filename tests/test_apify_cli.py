"""Credential boundary for optional Apify CLI discovery."""

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'plugins/mobile-app-builder-research/scripts/actor-search.mjs'


class ActorSearchTests(unittest.TestCase):
    def test_search_uses_isolated_cli_without_ambient_token(self):
        with tempfile.TemporaryDirectory() as directory:
            fake = Path(directory) / 'apify'
            fake.write_text('''#!/bin/sh
test -z "$APIFY_TOKEN" || exit 7
test "$APIFY_CLI_DISABLE_TELEMETRY" = 1 || exit 8
test "$1" = actors && test "$2" = search && test "$3" = "mobile ads" || exit 9
test "$4" = --json && test "$5" = --limit && test "$6" = 2 || exit 10
printf '{"items":[{"username":"sample","name":"actor","title":"Sample Actor","description":"Example"}],"count":1}'
''')
            fake.chmod(0o755)
            env = {**os.environ, 'PATH': f'{directory}:{os.environ.get("PATH", "")}',
                   'APIFY_TOKEN': 'ambient-token-must-not-forward'}
            result = subprocess.run([shutil.which('node'), str(SCRIPT), '--query', 'mobile ads',
                                     '--limit', '2'], capture_output=True, text=True, env=env)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('sample/actor', result.stdout)
            self.assertNotIn('ambient-token', result.stdout + result.stderr)

    def test_rejects_options_as_query(self):
        result = subprocess.run([shutil.which('node'), str(SCRIPT), '--query', '--token'],
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('token=', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
