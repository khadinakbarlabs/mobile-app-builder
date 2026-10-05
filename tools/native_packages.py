"""Publisher-only adapters; shared guidance comes from the installed core."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import zipfile

import yaml

from release import ROOT, SECRET_CONTENT, SECRET_FILE, check_names, frontmatter, validate_folder


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def metadata(skill, name, description):
    folder = skill / 'agents'
    folder.mkdir(exist_ok=True)
    short = description if len(description) <= 64 else description[:65].rsplit(' ', 1)[0][:64]
    (folder / 'openai.yaml').write_text(yaml.safe_dump({'interface': {
        'display_name': name.replace('-', ' ').title(),
        'short_description': short,
        'default_prompt': f'Use ${name} for the relevant app task and return a verified result.'}},
        sort_keys=False))


def export_edition(source, destination, host):
    source, destination = Path(source).resolve(), Path(destination).resolve()
    if host not in {'codex', 'cursor'}:
        raise ValueError('Unsupported host')
    if destination.exists():
        raise ValueError('Destination exists; preserve it or choose a fresh version')
    validate_folder(source, core=True)
    manifest = json.loads((source / '.claude-plugin/plugin.json').read_text())
    # Everything copied was already validated as installed core content by release.py.
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns('.claude-plugin'))
    artwork = destination / 'assets'
    artwork.mkdir()
    shutil.copyfile(source / '.claude-plugin/icon.png', artwork / 'logo.png')
    identity = {key: manifest[key] for key in
                ('name', 'version', 'description', 'author', 'homepage', 'repository', 'license', 'keywords')}
    # Portable skill inventories expect only executable entries in skills/.
    detailed = {path.name for path in (destination / 'skills').iterdir()
                if path.is_dir() and not (path / 'SKILL.md').exists()}
    original_files = [path for path in destination.rglob('*') if path.is_file()]

    def moved(path):
        relative = path.relative_to(destination)
        if len(relative.parts) >= 2 and relative.parts[0] == 'skills' and relative.parts[1] in detailed:
            return destination / 'workflows' / Path(*relative.parts[1:])
        return path

    (destination / 'workflows').mkdir()
    for name in sorted(detailed):
        shutil.move(destination / 'skills' / name, destination / 'workflows' / name)
    for original in original_files:
        current = moved(original)
        if current.suffix != '.md':
            continue

        def relocate_link(match):
            reference = match.group(1)
            target, separator, anchor = reference.partition('#')
            if not target or re.match(r'(?:https?://|mailto:)', target):
                return match.group(0)
            resolved = (original.parent / target).resolve()
            if not resolved.is_relative_to(destination.resolve()):
                raise ValueError('Escaping source resource')
            new_target = moved(resolved)
            return '](' + Path(os.path.relpath(new_target, current.parent)).as_posix() + (separator + anchor) + ')'

        current.write_text(re.sub(r'\]\(([^)\s]+)\)', relocate_link, current.read_text()))
    catalog_path = destination / 'agency/catalog.json'
    catalog = json.loads(catalog_path.read_text())
    for entry in catalog['skills']:
        entry['path'] = 'workflows/' + entry['id'] + '/guide.md'
    write_json(catalog_path, catalog)
    if host == 'codex':
        for command in sorted((destination / 'commands').glob('*.md')):
            text = command.read_text()
            fields, body = text.split('---', 2)[1:]
            fields = yaml.safe_load(fields)
            name = command.stem
            skill = destination / 'skills' / name
            skill.mkdir()
            # Command files move one level deeper; keep every reference contained.
            body = re.sub(r'(?<=\]\()\.\./', '../../', body)
            (skill / 'SKILL.md').write_text('---\nname: ' + name + '\ndescription: '
                + json.dumps(fields['description']) + '\n---\n' + body.lstrip())
            metadata(skill, name, fields['description'])
        shutil.rmtree(destination / 'commands')
        interface = {
            'displayName': 'Mobile App Builder', 'shortDescription': 'Build iOS, Android & web apps',
            'longDescription': 'Research, design, build, fix and grow apps in their existing stack. '
                               'Includes focused workflows, local inspection, recovery and reviewable continuity. '
                               'Account research and releases use separately authorized tools.',
            'developerName': manifest['author']['name'], 'category': 'Developer Tools',
            'capabilities': ['Interactive'],
            'websiteURL': manifest['homepage'],
            'privacyPolicyURL': manifest['repository'] + '/blob/main/plugins/mobile-app-builder/PRIVACY.md',
            'termsOfServiceURL': manifest['repository'] + '/blob/main/plugins/mobile-app-builder/TERMS.md',
            'defaultPrompt': ['Research a new app idea and define its first useful feature.',
                              'Fix this issue in my existing iOS, Android or web app.',
                              'Continue my app task from its accepted checkpoint.'],
            'brandColor': '#2154D8', 'composerIcon': './assets/logo.png', 'logo': './assets/logo.png'}
        write_json(destination / 'plugin.json', {
            '$schema': 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json', **identity,
            'extensions': {'com.openai': {'interface': interface}}})
        write_json(destination / '.codex-plugin/plugin.json', {**identity, 'skills': './skills/', 'interface': interface})
    else:
        identity['author'] = {'name': manifest['author']['name']}
        write_json(destination / '.cursor-plugin/plugin.json', {**identity, 'logo': './assets/logo.png'})
    readme = (destination / 'README.md').read_text()
    start = readme.index('## Install\n')
    end = readme.index('## Execution and data handling\n', start)
    instructions = ('Use the installed plugin or add this directory through a local marketplace. '
                    'The eight command shortcuts are preserved as skill aliases, including `$new-app` and `$improve-app`.'
                    if host == 'codex' else
                    'Copy this complete native package into the host’s supported local plugin folder, reload the window, '
                    'and confirm its 30 skills, eight commands and eight agents in Customize.')
    readme = readme[:start] + '## Install\n\n' + instructions + '\n\n' + readme[end:]
    if host == 'codex':
        readme = readme.replace('/mobile-app-builder:new-app', '$new-app').replace('/mobile-app-builder:improve-app', '$improve-app')
        readme = readme.replace('8 commands', '8 command aliases')
    (destination / 'README.md').write_text(readme)
    return validate_edition(destination, host)


def validate_edition(folder, host):
    folder = Path(folder)
    forbidden = {'.claude-plugin', '.cursor-plugin'} if host == 'codex' else {'.claude-plugin', '.codex-plugin', 'plugin.json'}
    if any((folder / name).exists() for name in forbidden):
        raise ValueError('Unrelated host adapter in native package')
    manifest_path = folder / ('plugin.json' if host == 'codex' else '.cursor-plugin/plugin.json')
    manifest = json.loads(manifest_path.read_text())
    if host == 'codex':
        if set(manifest) & {'skills', 'interface', 'mcpServers', 'apps'}:
            raise ValueError('Unsupported portable manifest field')
        legacy = json.loads((folder / '.codex-plugin/plugin.json').read_text())
        if any(legacy[key] != manifest[key] for key in ('name', 'version', 'description', 'repository')):
            raise ValueError('Native manifest version or identity drift')
        interface = manifest['extensions']['com.openai']['interface']
        if len(interface['shortDescription']) > 30 or interface != legacy['interface']:
            raise ValueError('Native interface mismatch')
        for key in ('composerIcon', 'logo'):
            if not (folder / interface[key]).is_file():
                raise ValueError('Missing artwork resource')
    entries = sorted(folder.rglob('*'))
    check_names([path.relative_to(folder) for path in entries])
    skills = []
    files = []
    for path in entries:
        if path.is_symlink() or SECRET_FILE.fullmatch(path.name) or path.name in {'.git', '__pycache__', 'node_modules'}:
            raise ValueError('Unsafe native package entry')
        if not path.is_file():
            continue
        data = path.read_bytes()
        if path.suffix != '.png':
            text = data.decode('utf-8')
            if SECRET_CONTENT.search(text):
                raise ValueError('Credential in native package')
            if path.name == 'SKILL.md':
                fields = frontmatter(text, path.parent.name)
                skills.append(fields['name'])
                metadata_path = path.parent / 'agents/openai.yaml'
                if not metadata_path.is_file() or '$' + fields['name'] not in metadata_path.read_text():
                    raise ValueError('Missing skill UI resource')
            for reference in re.findall(r'\]\(([^)\s]+)\)', text) if path.suffix == '.md' else []:
                target = reference.split('#', 1)[0]
                if not target or re.match(r'(?:https?://|mailto:)', target):
                    continue
                resource = (path.parent / target).resolve()
                if not resource.is_relative_to(folder.resolve()) or not resource.exists():
                    raise ValueError('Missing or escaping native resource: ' + path.relative_to(folder).as_posix())
        files.append({'path': path.relative_to(folder).as_posix(), 'sha256': hashlib.sha256(data).hexdigest()})
    commands = len(list((folder / 'commands').glob('*.md')))
    agents = len(list((folder / 'agents').glob('*.md')))
    if len(skills) + commands != 38 or agents != 8:
        raise ValueError('Native component inventory differs')
    return {'host': host, 'name': manifest['name'], 'version': manifest['version'],
            'skills': len(skills), 'commands': commands, 'agents': agents, 'files': files}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    reports = []
    for host in ('codex', 'cursor'):
        edition = args.output / host / 'mobile-app-builder'
        report = export_edition(ROOT / 'plugins/mobile-app-builder', edition, host)
        archive_path = args.output / f'mobile-app-builder-{host}-{report["version"]}.zip'
        with zipfile.ZipFile(archive_path, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
            for entry in report['files']:
                archive.write(edition / entry['path'], entry['path'])
        with zipfile.ZipFile(archive_path) as archive:
            if archive.testzip() is not None:
                raise ValueError('Native archive integrity failure')
            for entry in report['files']:
                if hashlib.sha256(archive.read(entry['path'])).hexdigest() != entry['sha256']:
                    raise ValueError('Native archive content differs')
        report.update({'archive': archive_path.name, 'sha256': hashlib.sha256(archive_path.read_bytes()).hexdigest()})
        reports.append(report)
    write_json(args.output / 'native-inventories.json', reports)
    print('Built and checked separate Codex and Cursor packages; installation and publication remain separate checks.')


if __name__ == '__main__':
    main()
