import importlib.util
import json
import os
from pathlib import Path
import shutil
import socket
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('release', ROOT / 'tools/release.py')
release = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release)


class ReleaseBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'sample-plugin'
        self.write('.claude-plugin/plugin.json', json.dumps({
            'name': 'sample-plugin', 'version': '1.0.0',
            'description': 'A fixture', 'author': {'name': 'Example'},
        }))
        self.write('README.md', 'Portable workflow instructions. ' * 45)
        self.write('skills/example/SKILL.md',
                   '---\nname: example\ndescription: A useful workflow\n---\n\nHelp with the workflow.\n')

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def test_full_inventory_and_reproducible_single_root_archive(self):
        report = release.validate_folder(self.root)
        self.assertEqual(report['skills'], ['example'])
        self.assertEqual(len(report['files']), 3)
        first, second = self.root.parent / 'one.zip', self.root.parent / 'two.zip'
        release.build_archive(self.root, first)
        release.build_archive(self.root, second)
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with zipfile.ZipFile(first) as archive:
            self.assertTrue(all(name.startswith('sample-plugin/') for name in archive.namelist()))
            self.assertEqual(archive.read('sample-plugin/skills/example/SKILL.md'),
                             (self.root / 'skills/example/SKILL.md').read_bytes())

    def test_rejects_symlink_even_when_target_exists(self):
        (self.root / 'linked.md').symlink_to(self.root / 'README.md')
        with self.assertRaisesRegex(ValueError, 'Symbolic'):
            release.validate_folder(self.root)

    @unittest.skipUnless(hasattr(os, 'mkfifo'), 'Named pipes require a Unix filesystem')
    def test_rejects_named_pipe_instead_of_omitting_it_from_inventory(self):
        os.mkfifo(self.root / 'unreadable.md')
        with self.assertRaisesRegex(ValueError, 'regular'):
            release.validate_folder(self.root)

    @unittest.skipUnless(hasattr(socket, 'AF_UNIX'), 'Unix sockets are unavailable')
    def test_rejects_socket_instead_of_omitting_it_from_inventory(self):
        with socket.socket(socket.AF_UNIX) as server:
            server.bind(str(self.root / 'file.sock'))
            with self.assertRaisesRegex(ValueError, 'regular'):
                release.validate_folder(self.root)

    def test_rejects_unreadable_binary_oversized_text_and_credentials(self):
        for name, data, expected in [('file.bin', b'\x00\xff', 'Unsupported'),
                                     ('huge.md', b'x' * (256 * 1024), '256 KiB'),
                                     ('.env.local', b'NOT_A_TOKEN=example', 'Credential')]:
            with self.subTest(name=name):
                path = self.root / name
                path.write_bytes(data)
                with self.assertRaisesRegex(ValueError, expected):
                    release.validate_folder(self.root)
                path.unlink()

    def test_rejects_escaping_markdown_reference(self):
        self.write('skills/example/SKILL.md',
                   '---\nname: example\ndescription: Useful\n---\n[Outside](../../../outside.md)\n')
        with self.assertRaisesRegex(ValueError, 'reference'):
            release.validate_folder(self.root)

    def test_markdown_can_link_to_an_installed_directory(self):
        self.write('README.md', 'A useful portable workflow. ' * 45 + '\n[Skills](skills/)\n')
        self.assertEqual(release.validate_folder(self.root)['skills'], ['example'])

    def test_rejects_duplicate_frontmatter_keys_and_description_lists(self):
        for frontmatter in ['name: example\nname: overwritten\ndescription: Useful',
                            'name: example\ndescription: [bad, description]']:
            with self.subTest(frontmatter=frontmatter):
                self.write('skills/example/SKILL.md', f'---\n{frontmatter}\n---\nBody\n')
                with self.assertRaises(ValueError):
                    release.validate_folder(self.root)

    def test_rejects_windows_case_collisions_and_reserved_names(self):
        with self.assertRaisesRegex(ValueError, 'collisi'):
            release.check_names(['README.md', 'readme.md'])
        self.write('con.md', 'Windows reserved name')
        with self.assertRaisesRegex(ValueError, 'Portable'):
            release.validate_folder(self.root)

    def test_rejects_all_windows_invalid_filename_characters(self):
        for char in '<>"|?*\\':
            with self.subTest(char=char), self.assertRaisesRegex(ValueError, 'Portable'):
                release.check_names(['bad' + char + 'name.md'])

    def test_missing_documented_helper_and_backtick_resource_are_rejected(self):
        for text in ['Run node scripts/missing.mjs', 'Read `references/missing.json`']:
            with self.subTest(text=text):
                self.write('README.md', 'Portable workflow instructions. ' * 45 + text)
                with self.assertRaisesRegex(ValueError, 'reference'):
                    release.validate_folder(self.root)

    def test_migration_rejects_false_source_hash_duplicates_and_false_unchanged(self):
        import hashlib
        data = (self.root / 'README.md').read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        source = {'fileCount': 1, 'files': [{'path': 'README.md', 'sha256': digest}]}
        original = {'source': 'README.md', 'sourceSha256': digest, 'target': 'README.md',
                    'targetSha256': digest, 'status': 'unchanged'}
        valid = {'files': [original.copy()]}
        release.validate_migration(self.root, valid, source)
        for mutation in ['sourcehash', 'duplicate', 'unchanged']:
            candidate = {'files': [original.copy()]}
            if mutation == 'sourcehash':
                candidate['files'][0]['sourceSha256'] = '0' * 64
            elif mutation == 'duplicate':
                candidate['files'].append(original.copy())
            else:
                changed = self.write('changed.md', 'Adapted document')
                candidate['files'][0]['target'] = 'changed.md'
                candidate['files'][0]['targetSha256'] = hashlib.sha256(changed.read_bytes()).hexdigest()
            with self.subTest(mutation=mutation), self.assertRaisesRegex(ValueError, 'Migration'):
                release.validate_migration(self.root, candidate, source)
        with self.assertRaisesRegex(ValueError, 'Migration'):
            release.validate_migration(self.root, valid, {'fileCount': 2, 'files': source['files'] * 2})

    def test_real_catalog_browser_loads_and_filters_web_workflows(self):
        import subprocess
        tool = ROOT / 'plugins/mobile-app-builder/scripts/agency.mjs'
        all_skills = json.loads(subprocess.check_output(['node', str(tool), '--json'], text=True))
        self.assertEqual(len(all_skills), 190)
        web_skills = json.loads(subprocess.check_output(['node', str(tool), '--platform', 'web', '--json'], text=True))
        self.assertEqual([item['id'] for item in web_skills], ['build-web-app'])

    def test_workflow_extensions_preserve_every_original_skill(self):
        previous = {'files': [{'path': 'skills/example/SKILL.md'}]}
        routes = [{'id': 'example', 'path': 'skills/example/guide.md',
                   'entrySkill': 'guide-example'}]
        self.write('skills/example/guide.md', 'Original guide\n')
        release.validate_preserved_skills(self.root, ['guide-example'], routes, previous)
        with self.assertRaisesRegex(ValueError, 'original'):
            release.validate_preserved_skills(self.root, ['guide-example'], [], previous)

    def test_real_core_has_fewer_entry_points_and_all_workflows_routed(self):
        core = ROOT / 'plugins/mobile-app-builder'
        report = release.validate_folder(core, core=True)
        catalog = json.loads((core / 'agency/catalog.json').read_text())
        source = json.loads((ROOT / 'migration/source.json').read_text())
        self.assertLess(len(report['skills']) + len(report['commands']), 40)
        self.assertLess(len(report['agents']), 10)
        self.assertGreaterEqual(len(report['commands']), 8)
        release.validate_preserved_skills(core, report['skills'], catalog['skills'], source)

    def test_core_refuses_mcp_or_environment_reading_helpers(self):
        self.write('.mcp.json', json.dumps({'apify': {'type': 'http', 'url': 'https://mcp.apify.com'}}))
        with self.assertRaisesRegex(ValueError, 'Core'):
            release.validate_folder(self.root, core=True)
        (self.root / '.mcp.json').unlink()
        self.write('scripts/read.mjs', 'console.log(process.env.EXAMPLE_TOKEN);')
        with self.assertRaisesRegex(ValueError, 'environment'):
            release.validate_folder(self.root, core=True)

    def test_core_refuses_network_and_subprocess_helpers(self):
        for source in ["await fetch('https://example.com');",
                       "import https from 'node:https';",
                       "import { execFile } from 'node:child_process';"]:
            with self.subTest(source=source):
                helper = self.write('scripts/connect.mjs', source)
                with self.assertRaisesRegex(ValueError, 'network or subprocess'):
                    release.validate_folder(self.root, core=True)
                helper.unlink()

    def test_core_keeps_listing_metadata_and_artwork_outside_installed_root(self):
        manifest_path = self.root / '.claude-plugin/plugin.json'
        manifest = json.loads(manifest_path.read_text())
        manifest['icon'] = './assets/logo.png'
        manifest_path.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, 'Directory listing fields'):
            release.validate_folder(self.root, core=True)
        del manifest['icon']
        manifest_path.write_text(json.dumps(manifest))
        asset = self.root / 'assets/logo.png'
        asset.parent.mkdir(parents=True)
        asset.write_bytes(b'not-a-png')
        with self.assertRaisesRegex(ValueError, 'Directory artwork'):
            release.validate_folder(self.root, core=True)
        asset.unlink()
        shutil.copyfile(ROOT / 'migration/previous-assets/mobile-app-builder-logo-v8.png',
                        self.root / '.claude-plugin/icon.png')
        self.assertEqual(release.validate_folder(self.root, core=True)['skills'], ['example'])

    def test_documented_build_config_cannot_serialize_credentials(self):
        for key, value in [('SENTRY_AUTH_TOKEN', '@sentry-auth-token'),
                           ('SERVICE_API_KEY', '<replace-with-secret>'),
                           ('CLIENT_SECRET', '${CLIENT_SECRET}'),
                           ('EXPO_PUBLIC_SERVICE_API_KEY', '<replace-with-secret>'),
                           ('EXPO_PUBLIC_FIREBASE_API_KEY', 'not-a-documented-placeholder')]:
            with self.subTest(key=key):
                example = {'build': {'production': {'env': {key: value}}}}
                self.write('docs/build.md', '```json\n' + json.dumps(example) + '\n```\n')
                with self.assertRaisesRegex(ValueError, 'documented build environment'):
                    release.validate_folder(self.root, core=True)

    def test_documented_build_config_allows_public_values_and_environment_selection(self):
        example = {'build': {'production': {'environment': 'production', 'env': {
            'EXPO_PUBLIC_API_URL': 'https://api.example.com', 'APP_VARIANT': 'production',
            'EXPO_PUBLIC_FIREBASE_API_KEY': '<firebase-public-web-api-key>'}}}}
        self.write('docs/build.md', '```json\n' + json.dumps(example) + '\n```\n')
        self.assertEqual(release.validate_folder(self.root, core=True)['skills'], ['example'])

    def test_research_auth_is_explicit_and_fixed_to_apify(self):
        manifest = json.loads((self.root / '.claude-plugin/plugin.json').read_text())
        manifest['userConfig'] = {'apify_token': {
            'type': 'string', 'title': 'Apify token', 'description': 'Explicit user token',
            'sensitive': True, 'required': True}}
        self.write('.claude-plugin/plugin.json', json.dumps(manifest))
        self.write('.mcp.json', json.dumps({'apify': {
            'type': 'http', 'url': 'https://mcp.apify.com?tools=search-actors,call-actor',
            'headers': {'Authorization': 'Bearer ${user_config.apify_token}'}}}))
        self.assertEqual(release.validate_folder(self.root)['connectors'], ['apify'])
        manifest['userConfig']['apify_token']['sensitive'] = False
        self.write('.claude-plugin/plugin.json', json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, 'sensitive'):
            release.validate_folder(self.root)

    def test_core_rejects_authenticated_research_cli_instructions(self):
        self.write('docs/research.md', 'Run `apify actors start example/actor` after signing in.\n')
        with self.assertRaisesRegex(ValueError, 'authenticated research CLI'):
            release.validate_folder(self.root, core=True)

    def test_core_rejects_inline_bearer_forwarding_examples(self):
        self.write('docs/network.md', 'headers: { Authorization: `Bearer ${token}` }\n')
        with self.assertRaisesRegex(ValueError, 'inline bearer forwarding'):
            release.validate_folder(self.root, core=True)

    def test_broken_local_module_import_is_rejected(self):
        self.write('scripts/tool.mjs', "import { example } from './missing.mjs';\n")
        with self.assertRaisesRegex(ValueError, 'module'):
            release.validate_folder(self.root)


if __name__ == '__main__':
    unittest.main()
