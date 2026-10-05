"""Resource and entry compatibility checks for generated host editions."""

import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import native_packages


class NativePackageTests(unittest.TestCase):
    def test_codex_preserves_guides_and_converts_all_command_aliases(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / 'mobile-app-builder'
            native_packages.export_edition(ROOT / 'plugins/mobile-app-builder', target, 'codex')
            manifest = json.loads((target / 'plugin.json').read_text())
            self.assertEqual(manifest['name'], 'mobile-app-builder')
            self.assertNotIn('skills', manifest)
            self.assertNotIn('interface', manifest)
            self.assertEqual(len(list((target / 'skills').glob('*/SKILL.md'))), 38)
            self.assertTrue((target / 'workflows/eas-submit-play/guide.md').is_file())
            alias = (target / 'skills/build-app/SKILL.md').read_text()
            self.assertIn('../../docs/INTELLIGENT-WORKFLOW.md', alias)
            self.assertIn('$build-app', (target / 'skills/build-app/agents/openai.yaml').read_text())
            self.assertFalse((target / '.claude-plugin').exists())
            self.assertFalse((target / '.cursor-plugin').exists())
            self.assertEqual(native_packages.validate_edition(target, 'codex')['skills'], 38)

    def test_cursor_retains_native_commands_and_agents_with_separate_manifest(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / 'mobile-app-builder'
            native_packages.export_edition(ROOT / 'plugins/mobile-app-builder', target, 'cursor')
            self.assertEqual(len(list((target / 'skills').glob('*/SKILL.md'))), 30)
            self.assertEqual(len(list((target / 'commands').glob('*.md'))), 8)
            self.assertEqual(len(list((target / 'agents').glob('*.md'))), 8)
            self.assertFalse((target / '.claude-plugin').exists())
            self.assertFalse((target / '.codex-plugin').exists())
            self.assertEqual(native_packages.validate_edition(target, 'cursor')['commands'], 8)

    def test_native_validation_rejects_resource_loss_and_version_drift(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / 'mobile-app-builder'
            native_packages.export_edition(ROOT / 'plugins/mobile-app-builder', target, 'codex')
            (target / 'docs/INTELLIGENT-WORKFLOW.md').unlink()
            with self.assertRaisesRegex(ValueError, 'resource'):
                native_packages.validate_edition(target, 'codex')
