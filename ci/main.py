import os, yaml, logging
from pytablewriter import MarkdownTableWriter

# Setup logging
logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initial constants
__scriptdir = os.path.dirname(os.path.realpath(__file__))
bypasses_file = os.path.join(__scriptdir, '..', 'manifests', 'bypasses.yaml')
apps_dir = os.path.join(__scriptdir, '..', 'manifests', 'apps')

with open(bypasses_file) as file:
    bypasses = yaml.safe_load(file)

# List all files in manifests/apps
table_matrix = list()
apps_files = [os.path.join(apps_dir, f) for f in os.listdir(apps_dir) if os.path.isfile(os.path.join(apps_dir, f))]
for app_file in apps_files:
    with open(app_file, encoding='utf-8') as file:
        app = yaml.safe_load(file.read())

    if app['bypasses'] is None:
        row = list()
        row.append(f"[{app['name']}]({app['uri']})") 
        row.append('')
        row.append("No known bypass")
        row.append("")
        table_matrix.append(row)
        continue

    for bypass in app['bypasses']:
        row = list()
        row.append(f"[{app['name']}]({app['uri']})") 
        row.append(bypass['version'] if 'version' in bypass else '')

        if 'name' in bypass:
            bypass_tweak = f"{bypass['name']}" 
            bypass_tweak_repo = f"[repo]({bypasses[bypass['name']]['repo']})" if 'repo' in bypasses[bypass['name']] else None
            bypass_tweak_guide = f"[repo]({bypasses[bypass['name']]['guide']})" if 'guide' in bypasses[bypass['name']] else None

            bypass_tweak_info = f" ({', '.join(filter(None, [bypass_tweak_repo, bypass_tweak_guide]))})" if (bypass_tweak_repo or bypass_tweak_guide) else ''
            row.append(bypass_tweak + bypass_tweak_info)

            notes_from_bypass = bypasses[bypass['name']]['notes'] if 'notes' in bypasses[bypass['name']] else ''
            notes_from_manifest = bypass['notes'] if 'notes' in bypass else ''
            row.append(notes_from_bypass + notes_from_manifest)
        elif 'notes' in bypass:
            logger.warning('Bypass name not specified, printing notes only')
            row.append('')
            row.append(bypass['notes'] if 'notes' in bypass else '')
        else: 
            logger.error('Neither name nor notes were supplied for this bypass!')
            continue
        table_matrix.append(row)
table_matrix.sort(key=lambda app: app[0])

writer = MarkdownTableWriter(
    headers=["App", "Version", "Bypass", "Notes"],
    value_matrix=table_matrix,
    margin=1  # add a whitespace for both sides of each cell
)
writer.write_table()



