import os, yaml, logging, argparse
from pytablewriter import MarkdownTableWriter

# Setup logging
logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--print', action='store_true', help='Print result to stdout')
args = parser.parse_args()

# Initial constants
__scriptdir = os.path.dirname(os.path.realpath(__file__))
bypasses_file = os.path.join(__scriptdir, '..', 'manifests', 'bypasses.yaml')
apps_dir = os.path.join(__scriptdir, '..', 'manifests', 'apps')

with open(bypasses_file, encoding='utf-8') as file:
    bypasses = yaml.safe_load(file)

# List all files in manifests/apps
table_matrix = list()
apps_files = [os.path.join(apps_dir, f) for f in os.listdir(apps_dir) if os.path.isfile(os.path.join(apps_dir, f))]
for app_file in apps_files:
    with open(app_file, encoding='utf-8') as file:
        app = yaml.safe_load(file.read())
    if app['bypasses'] is None:
        table_matrix.append([f"[{app['name']}]({app['uri']})", '', 'No known bypass', ''])
        continue
    
    bypass_versions = str()
    bypass_tweaks = str()
    bypass_notes = str()
    for bypass in app['bypasses']:
        bypass_versions += f"{bypass['version']}<br>" if 'version' in bypass else '<br>'

        if 'name' in bypass:
            bypass_tweak = f"[{bypass['name']}]({bypasses[bypass['name']]['guide']})" if 'guide' in bypasses[bypass['name']] else bypass['name']
            bypass_tweak_repo = f" ([repo](https://sharerepo.stkc.win/?repo={bypasses[bypass['name']]['repo']}))" if 'repo' in bypasses[bypass['name']] else None
            bypass_tweaks += bypass_tweak + bypass_tweak_repo + '<br>'

            notes_from_version = "Use AppStore++ ([repo](https://sharerepo.stkc.win/?repo=https://cokepokes.github.io)) to downgrade.<br>" if ('version' in bypass and bypass['name'] != "AppStore++") else ''
            notes_from_bypass = f"{bypasses[bypass['name']]['notes']} " if 'notes' in bypasses[bypass['name']] else ''
            notes_from_manifest = bypass['notes'] if 'notes' in bypass else ''
            bypass_notes += notes_from_version + (f"**{bypass['name']}**: " + notes_from_bypass + notes_from_manifest + '<br>' if (notes_from_bypass or notes_from_manifest) else '')
        elif 'notes' in bypass:
            logger.warning('Bypass name not specified, printing notes only')
            bypass_tweaks += ''
            bypass_notes += f"{bypass['notes']}<br>" if 'notes' in bypass else '<br>'
        else: 
            logger.error('Neither name nor notes were supplied for this bypass!')
            continue  
    table_matrix.append([f"[{app['name']}]({app['uri']})", bypass_versions, bypass_tweaks, bypass_notes])
table_matrix.sort(key=lambda app: app[0].lower())

writer = MarkdownTableWriter(
    headers=["App", "Version", "Bypass", "Notes"],
    value_matrix=table_matrix,
    margin=1  # add a whitespace for both sides of each cell
)

# Writing to the actual app-list.md
if not args.print:
    headers_dir = os.path.join(__scriptdir, 'md-headers')
    app_list_md = os.path.join(__scriptdir, '..', 'README.md')
    with open(os.path.join(headers_dir, 'app-list.md'), encoding='utf-8', mode='r') as infile, open(app_list_md, encoding='utf-8', mode='w') as outfile:
        outfile.write(infile.read())
        outfile.write('\n\n')
        outfile.write(writer.dumps())
else:
    writer.write_table()