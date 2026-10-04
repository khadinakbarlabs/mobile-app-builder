"""Behavior tests for the local context and visual-report helpers."""

import json
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'plugins/mobile-app-builder/scripts'


def run(script, *args, expected=0):
    result = subprocess.run(['node', str(SCRIPTS / script), *map(str, args)],
                            text=True, capture_output=True)
    if result.returncode != expected:
        raise AssertionError(f'{script}: exit {result.returncode}, expected {expected}\n'
                             f'stdout: {result.stdout}\nstderr: {result.stderr}')
    return result


class ProductIntelligenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_expo_project_snapshot_is_bounded_and_does_not_echo_configuration(self):
        app = self.root / 'sample-app'
        app.mkdir()
        (app / 'package.json').write_text(json.dumps({
            'name': 'sample-app',
            'dependencies': {'expo': '^54.0.0', 'react-native-web': '^0.21.0'},
            'scripts': {'test': 'echo private-path', 'lint': 'eslint .'},
            'privateField': 'do-not-echo',
        }))
        (app / 'app.json').write_text(json.dumps({'expo': {
            'name': 'Sample', 'ios': {'bundleIdentifier': 'private.bundle.id'},
        }}))
        (app / '.env').write_text('SECRET_VALUE=do-not-echo')
        report = json.loads(run('inspect-project.mjs', app, '--goal', 'Fix onboarding').stdout)
        self.assertEqual(report['stage'], 'existing-app')
        self.assertEqual(report['platforms'], ['ios', 'android', 'web'])
        self.assertIn('Expo', report['frameworks'])
        self.assertEqual(report['availableChecks'], ['lint', 'test'])
        self.assertEqual(report['requestedOutcome'], 'Fix onboarding')
        self.assertNotIn('do-not-echo', json.dumps(report))
        self.assertNotIn('private.bundle.id', json.dumps(report))
        self.assertNotIn('private-path', json.dumps(report))

    def test_empty_project_starts_as_an_idea_and_symlink_manifest_fails(self):
        app = self.root / 'new-idea'
        app.mkdir()
        report = json.loads(run('inspect-project.mjs', app).stdout)
        self.assertEqual(report['stage'], 'idea-or-unknown')
        self.assertEqual(report['platforms'], [])
        external = self.root / 'external.json'
        external.write_text('{"dependencies":{"expo":"54"}}')
        (app / 'package.json').symlink_to(external)
        result = run('inspect-project.mjs', app, expected=1)
        self.assertIn('symbolic link', result.stderr.lower())

    def test_visual_report_escapes_user_text_and_stays_self_contained(self):
        source = self.root / 'report.json'
        source.write_text(json.dumps({
            'title': 'Onboarding <script>alert(1)</script>',
            'project': 'Example app',
            'summary': 'Users leave before activation.',
            'signals': [{'label': 'Activation', 'value': '28%'}],
            'findings': [{'title': 'Missing empty state', 'status': 'attention',
                          'detail': 'The first screen has no empty state.',
                          'evidence': 'Local screen review'}],
            'nextActions': [{'title': 'Add empty state', 'why': 'Clearer first result',
                             'priority': 'high'}],
            'limitations': ['No physical device test yet.'],
        }))
        output = self.root / 'report.html'
        run('render-report.mjs', source, '--output', output)
        html = output.read_text()
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', html)
        self.assertNotIn('<script>', html)
        self.assertIn('Activation', html)
        self.assertIn('Add empty state', html)
        self.assertIn('No physical device test yet.', html)
        self.assertNotIn('http://', html)
        self.assertNotIn('https://', html)
        self.assertIn('@media', html)
        self.assertIn('aria-label', html)
        self.assertIn('lang="en"', html)
        self.assertIn('utf-8', html.lower())
        self.assertIn('already exists', run('render-report.mjs', source, '--output', output,
                                             expected=1).stderr.lower())

    def test_visual_report_rejects_invalid_structure_and_sensitive_values(self):
        source = self.root / 'bad.json'
        output = self.root / 'bad.html'
        source.write_text(json.dumps({'title': 'Missing required fields'}))
        self.assertIn('summary', run('render-report.mjs', source, '--output', output,
                                     expected=1).stderr.lower())
        self.assertFalse(output.exists())
        source.write_text(json.dumps({'title': 'Bad', 'summary': 'fine',
                                      'signals': [{'label': 'Token', 'value': 'sk-' + 'x' * 30}]}))
        self.assertIn('sensitive', run('render-report.mjs', source, '--output', output,
                                       expected=1).stderr.lower())
        self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
