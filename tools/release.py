"""Publisher-only validation and reproducible packaging for the Anthropic edition."""

import hashlib
import json
from pathlib import Path
import re
import tempfile
from urllib.parse import unquote, urlparse
import zipfile

from PIL import Image
import yaml


ROOT = Path(__file__).resolve().parents[1]
CORE = 'mobile-app-builder'
RESEARCH = 'mobile-app-builder-research'
PLUGINS = (CORE, RESEARCH)
TEXT_TYPES = {'.md', '.json', '.mjs', '.txt', '.yaml', '.yml'}
ID = re.compile(r'[a-z0-9][a-z0-9-]{0,62}[a-z0-9]|[a-z0-9]')
SEMVER = re.compile(r'\d+\.\d+\.\d+')
RESERVED = re.compile(r'(?:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?', re.I)
SECRET_FILE = re.compile(r'(?:\.env.*|\.dev\.vars.*|credentials.*|service-account.*|GoogleService-Info\.plist|google-services\.json|.*\.(?:p8|p12|pem|key|jks|keystore))', re.I)
SECRET_CONTENT = re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:sk-[A-Za-z0-9_-]{16,}|apify_api_[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{20,})\b')
ENV_READ = re.compile(r'process\s*\.\s*env|os\s*\.\s*environ|\$(?:\{)?[A-Z_]*(?:TOKEN|SECRET|PASSWORD|API_KEY)')
CORE_OUTBOUND = re.compile(
    r'\b(?:fetch\s*\(|new\s+WebSocket\s*\(|(?:from|import\s*\(|require\s*\()\s*[\'\"]'
    r'(?:node:)?(?:https?|net|tls|dgram|child_process)(?:/[^\'\"]*)?[\'\"])', re.I)
PRIVATE_ENV_KEY = re.compile(r'(?:^|_)(?:TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)(?:$|_)', re.I)
# Firebase client keys are public app configuration; allow only this fake example,
# never arbitrary values or a blanket EXPO_PUBLIC_* credential exception.
PUBLIC_ENV_EXAMPLES = {'EXPO_PUBLIC_FIREBASE_API_KEY': '<firebase-public-web-api-key>'}
DIRECTORY_LISTING_KEYS = {'icon', 'documentationUrl', 'supportUrl', 'privacyPolicyUrl', 'termsOfServiceUrl'}


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate YAML keys rather than silently overwriting a value."""


def unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError('Duplicate YAML key')
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def check_names(paths):
    seen = set()
    for path in paths:
        text = Path(path).as_posix()
        if text.casefold() in seen:
            raise ValueError('Case collision in plugin files')
        seen.add(text.casefold())
        for part in Path(path).parts:
            if (part.endswith((' ', '.')) or any(char in part for char in '<>:"|?*\\') or RESERVED.fullmatch(part)
                    or any(ord(char) < 32 for char in part)):
                raise ValueError('Portable file name required')


def contained_file(base, target, label, allow_directory=False):
    resolved = target.resolve()
    valid_type = resolved.is_file() or (allow_directory and resolved.is_dir())
    if not resolved.is_relative_to(base.resolve()) or not valid_type:
        relative = target.relative_to(base).as_posix() if target.is_relative_to(base) else target.name
        raise ValueError(f'Missing or escaping {label}: {relative}')


def frontmatter(text, identifier):
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
    if not match:
        raise ValueError('Missing component frontmatter')
    try:
        value = yaml.load(match[1], Loader=UniqueLoader)
    except yaml.YAMLError as error:
        raise ValueError('Malformed component frontmatter') from error
    if not isinstance(value, dict) or value.get('name') != identifier:
        raise ValueError('Component name must match its file or folder')
    if not isinstance(value.get('description'), str) or not value['description'].strip():
        raise ValueError('Component description must be text')
    return value


def command_frontmatter(text):
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
    if not match:
        raise ValueError('Missing command frontmatter')
    value = yaml.load(match[1], Loader=UniqueLoader)
    if not isinstance(value, dict) or not isinstance(value.get('description'), str) or not value['description'].strip():
        raise ValueError('Command description is required')


def validate_connectors(folder, manifest):
    config = folder / '.mcp.json'
    if not config.exists():
        return []
    servers = json.loads(config.read_text())
    if not isinstance(servers, dict) or set(servers) != {'apify'}:
        raise ValueError('Only the declared Apify connector belongs in this edition')
    server = servers['apify']
    parsed = urlparse(server.get('url', ''))
    if (server.get('type') != 'http' or parsed.scheme != 'https'
            or parsed.netloc != 'mcp.apify.com' or parsed.path not in {'', '/'}):
        raise ValueError('Research destination must be the declared HTTPS Apify endpoint')
    if set(server) != {'type', 'url', 'headers'} or server['headers'] != {
            'Authorization': 'Bearer ${user_config.apify_token}'}:
        raise ValueError('Research must use an explicit user_config header')
    option = manifest.get('userConfig', {}).get('apify_token', {})
    if (option.get('type') != 'string' or option.get('sensitive') is not True
            or option.get('required') is not True or 'default' in option):
        raise ValueError('Research token must be a required sensitive user option without a default')
    return sorted(servers)


def validate_documented_build_environments(text, relative):
    """Keep copyable JSON build examples from embedding private credentials."""
    def inspect(value):
        if isinstance(value, dict):
            environment = value.get('env')
            if isinstance(environment, dict):
                for key, example in environment.items():
                    if PRIVATE_ENV_KEY.search(key) and not (
                            key in PUBLIC_ENV_EXAMPLES and example == PUBLIC_ENV_EXAMPLES[key]):
                        raise ValueError(f'Credential in documented build environment: {relative}: {key}')
            for child in value.values():
                inspect(child)
        elif isinstance(value, list):
            for child in value:
                inspect(child)

    for example in re.findall(r'^```json\s*\n(.*?)^```\s*$', text, re.M | re.S):
        try:
            value = json.loads(example)
        except json.JSONDecodeError:
            # Partial examples are not executable JSON configurations.
            continue
        inspect(value)


def validate_folder(folder, core=False):
    folder = Path(folder)
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError('Plugin root must be a regular directory')
    entries = sorted(folder.rglob('*'))
    check_names([path.relative_to(folder) for path in entries])
    for path in entries:
        if path.is_symlink():
            raise ValueError('Symbolic links are not installed components')
        if not path.is_file() and not path.is_dir():
            raise ValueError('Installed entries must be regular files or directories')
        if SECRET_FILE.fullmatch(path.name):
            raise ValueError('Credential-shaped file is forbidden')
        if path.name in {'.git', '.DS_Store', 'node_modules', 'dist', '__pycache__', '.gitattributes'}:
            raise ValueError('Publisher/system files must stay outside the plugin')
    manifest = json.loads((folder / '.claude-plugin/plugin.json').read_text())
    if (not ID.fullmatch(manifest.get('name', ''))
            or not SEMVER.fullmatch(manifest.get('version', ''))
            or not manifest.get('description') or not manifest.get('author', {}).get('name')):
        raise ValueError('Plugin identity is incomplete')
    if core and (set(manifest) & {'mcpServers', 'hooks', 'dependencies', 'userConfig'}
                 or (folder / '.mcp.json').exists() or (folder / 'hooks').exists()):
        raise ValueError('Core must not declare connectors, hooks, dependencies or credentials')
    if core and set(manifest) & DIRECTORY_LISTING_KEYS:
        raise ValueError('Directory listing fields must stay out of the installed core manifest')
    skills, agents, commands, inventory = [], [], [], []
    for path in entries:
        if not path.is_file():
            continue
        relative = path.relative_to(folder)
        data = path.read_bytes()
        if len(data) >= 5 * 1024 * 1024:
            raise ValueError('Plugin file exceeds the directory limit')
        if core and path.suffix == '.png' and relative.as_posix() != '.claude-plugin/icon.png':
            raise ValueError('Directory artwork must stay outside the installed plugin root except the default icon')
        if path.suffix == '.png':
            with Image.open(path) as image:
                if image.format != 'PNG':
                    raise ValueError('Image must be a complete PNG')
                if core and relative.as_posix() == '.claude-plugin/icon.png' and (
                        image.width != image.height or not 512 <= image.width <= 2048 or len(data) >= 2 * 1024 * 1024):
                    raise ValueError('Default directory icon must be square, 512-2048 pixels, under 2 MiB')
                image.verify()
            with Image.open(path) as image:
                image.load()
        else:
            if path.suffix not in TEXT_TYPES and path.name != 'LICENSE':
                raise ValueError('Unsupported file type in plugin')
            if len(data) >= 256 * 1024:
                raise ValueError('Text file must be below 256 KiB')
            try:
                text = data.decode('utf-8', errors='strict')
            except UnicodeDecodeError as error:
                raise ValueError('Plugin text is not readable UTF-8') from error
            if '\x00' in text or SECRET_CONTENT.search(text):
                raise ValueError('Unreadable text or credential in plugin content')
            if path.suffix == '.json':
                json.loads(text)
            if core and path.suffix == '.mjs' and ENV_READ.search(text):
                raise ValueError('Core helper must not read installer environment credentials')
            if core and path.suffix == '.mjs' and CORE_OUTBOUND.search(text):
                raise ValueError('Core helper must not use network or subprocess access')
            if path.suffix == '.md':
                if core:
                    validate_documented_build_environments(text, relative)
                resource_patterns = [
                    r'\b(?:node|python3)\s+["\']?((?:\./)?scripts/[A-Za-z0-9_./-]+\.(?:mjs|js|py|sh))',
                    r'`((?:references|scripts)/[A-Za-z0-9_./-]+\.(?:md|json|yaml|mjs|js|py|sh))`',
                ]
                for pattern in resource_patterns:
                    for reference in re.findall(pattern, text):
                        candidates = [path.parent / reference, folder / reference]
                        if not any(candidate.is_file() and candidate.resolve().is_relative_to(folder.resolve())
                                   for candidate in candidates):
                            raise ValueError(f'Missing documented resource reference: {relative}: {reference}')
                for reference in re.findall(r'\]\(([^)\s]+)\)', text):
                    target = reference.strip('<>').split('#', 1)[0]
                    if not target or re.match(r'(?:https?://|mailto:)', target):
                        continue
                    contained_file(folder, path.parent / unquote(target), 'Markdown reference', allow_directory=True)
            if path.suffix == '.mjs':
                for reference in re.findall(r'(?:from\s*|import\s*)[\'"](\.[^\'"]+)[\'"]', text):
                    contained_file(folder, path.parent / reference, 'local module')
            if relative.parts[:1] == ('skills',) and path.name == 'SKILL.md':
                frontmatter(text, path.parent.name)
                skills.append(path.parent.name)
            if relative.parts[:1] == ('agents',) and path.suffix == '.md':
                frontmatter(text, path.stem)
                agents.append(path.stem)
            if relative.parts[:1] == ('commands',) and path.suffix == '.md':
                command_frontmatter(text)
                commands.append(path.stem)
        inventory.append({'path': relative.as_posix(), 'bytes': len(data),
                          'sha256': hashlib.sha256(data).hexdigest()})
    if len(inventory) > 512:
        raise ValueError('Plugin must contain at most 512 files')
    prose = re.sub(r'```.*?```', '', (folder / 'README.md').read_text(), flags=re.S)
    if len(prose.split()) < 40:
        raise ValueError('Plugin README requires at least 40 words')
    return {'name': manifest['name'], 'version': manifest['version'],
            'skills': sorted(skills), 'agents': sorted(agents), 'commands': sorted(commands), 'files': inventory,
            'connectors': validate_connectors(folder, manifest), 'directoryApproval': False}


def build_archive(folder, destination):
    folder, destination = Path(folder), Path(destination)
    report = validate_folder(folder, core=folder.name == CORE)
    with zipfile.ZipFile(destination, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for entry in report['files']:
            info = zipfile.ZipInfo(folder.name + '/' + entry['path'], (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, (folder / entry['path']).read_bytes())
    with zipfile.ZipFile(destination) as archive:
        if archive.testzip() is not None:
            raise ValueError('Archive integrity failed')
        for entry in report['files']:
            if hashlib.sha256(archive.read(folder.name + '/' + entry['path'])).hexdigest() != entry['sha256']:
                raise ValueError('Archive does not match its inventory')
    return {**report, 'archive': destination.name,
            'sha256': hashlib.sha256(destination.read_bytes()).hexdigest()}


def validate_migration(root, migration, source):
    originals = source['files']
    mapped = migration['files']
    expected = {entry['path']: entry['sha256'] for entry in originals}
    actual = {entry['source'] for entry in mapped}
    if (len(expected) != len(originals) or len(actual) != len(mapped)
            or source['fileCount'] != len(originals) or actual != set(expected)):
        raise ValueError('Migration inventory must uniquely account for every previous file')
    for entry in mapped:
        if entry['sourceSha256'] != expected[entry['source']]:
            raise ValueError('Migration source hash differs from the previous inventory')
        if entry['status'] not in {'unchanged', 'adapted', 'relocated'}:
            raise ValueError('Migration status is unrecognized')
        if entry['status'] in {'unchanged', 'relocated'} and entry['targetSha256'] != entry['sourceSha256']:
            raise ValueError('Migration claims preserved bytes that differ from the original')
        target = Path(root) / entry['target']
        contained_file(Path(root), target, 'migration target')
        if hashlib.sha256(target.read_bytes()).hexdigest() != entry['targetSha256']:
            raise ValueError('Migration target differs from the recorded content')


def validate_preserved_skills(root, current, routes, source):
    original = {Path(entry['path']).parent.name for entry in source['files']
                if entry['path'].startswith('skills/') and entry['path'].endswith('/SKILL.md')}
    by_id = {entry['id']: entry for entry in routes}
    if len(by_id) != len(routes) or not original.issubset(by_id):
        raise ValueError('Every original workflow must have a unique route')
    for identifier, entry in by_id.items():
        if entry.get('entrySkill') not in current or entry.get('path') != f'skills/{identifier}/guide.md':
            raise ValueError('Every original workflow must route to an installed entry skill and guide')
        contained_file(Path(root), Path(root) / entry['path'], 'workflow guide')


def validate_repository(root=ROOT):
    root = Path(root)
    if list(root.glob('.gitattributes')) or list((root / 'plugins').glob('.gitattributes')):
        raise ValueError('Parent Git attributes may rewrite the installed source')
    reports = [validate_folder(root / 'plugins' / name, core=name == CORE) for name in PLUGINS]
    core = reports[0]
    catalog = json.loads((root / 'plugins' / CORE / 'agency/catalog.json').read_text())
    if not 0 < len(core['skills']) + len(core['commands']) < 40 or not 0 < len(core['agents']) < 10 or len(core['commands']) < 8:
        raise ValueError('Consolidated entry-point limits or command set are incomplete')
    if sorted({item['entrySkill'] for item in catalog['skills']}) != core['skills']:
        raise ValueError('Every entry skill must serve a catalog workflow')
    if sorted({agent for dept in catalog['departments'] for agent in dept['agents']}) != core['agents']:
        raise ValueError('The full migrated agent team must remain discoverable')
    if len(catalog['departments']) != 8:
        raise ValueError('The specialist classification was lost')
    taxonomy = json.loads((root / 'plugins' / CORE / 'agency/taxonomy.json').read_text())
    classified = [(skill, group['department'], group['id'])
                  for group in taxonomy['groups'] for skill in group['skills']]
    expected = [(skill['id'], skill['department'], skill['category']) for skill in catalog['skills']]
    if (sorted(classified) != sorted(expected)
            or taxonomy['platforms'] != {skill['id']: skill['platform'] for skill in catalog['skills']}):
        raise ValueError('Workflow taxonomy differs from the installed catalog')
    marketplace = json.loads((root / '.claude-plugin/marketplace.json').read_text())
    if {entry['name']: entry['source'] for entry in marketplace['plugins']} != {
            name: './plugins/' + name for name in PLUGINS}:
        raise ValueError('Marketplace must point at the exact two installed roots')
    migration = json.loads((root / 'migration/report.json').read_text())
    source = json.loads((root / 'migration/source.json').read_text())
    validate_preserved_skills(root / 'plugins' / CORE, core['skills'], catalog['skills'], source)
    validate_migration(root, migration, source)
    return reports


def main():
    reports = validate_repository()
    version = reports[0]['version']
    parent = ROOT / 'dist'
    parent.mkdir(exist_ok=True)
    destination = parent / version
    if destination.exists():
        raise ValueError('Release already exists; choose a new version or a new output directory')
    with tempfile.TemporaryDirectory(prefix='release-', dir=parent) as temporary:
        stage = Path(temporary)
        built = [build_archive(ROOT / 'plugins' / name,
                 stage / f'{name}-{report["version"]}.zip')
                 for name, report in zip(PLUGINS, reports)]
        (stage / 'inventories.json').write_text(json.dumps(built, indent=2) + '\n')
        (stage / 'CHECKSUMS.txt').write_text(''.join(item['sha256'] + '  ' + item['archive'] + '\n' for item in built))
        stage.rename(destination)
    print(f'Built {len(built)} independently installable Claude packages; directory approval remains unverified.')


if __name__ == '__main__':
    main()
