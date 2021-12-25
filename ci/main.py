import os, yaml
from pytablewriter import MarkdownTableWriter

# Initial constants
__scriptdir = os.path.dirname(os.path.realpath(__file__))
bypasses_file = os.path.join(__scriptdir, '..', 'manifests', 'bypasses.yaml')
apps_dir = os.path.join(__scriptdir, '..', 'manifests', 'apps')


with open(bypasses_file) as file:
    bypasses = yaml.safe_load(file)

# List all files in manifests/apps
table_matrix = list()
apps_files = [os.path.join(apps_dir, f) for f in os.listdir(apps_dir) if os.path.isfile(os.path.join(apps_dir, f))]
apps_files.sort()
for app_file in apps_files:
    with open(app_file) as file:
        app = yaml.safe_load(file)
        for bypass in app['bypasses']:
            row = [f"[{app['name']}]({app['uri']})", 
                    f"{bypass['version'] if 'version' in bypass else ''}",
                    f"{bypass['name']} ([repo]({bypasses[bypass['name']]['repo']}))",
                    f"{bypass['notes'] if 'notes' in bypass else ''}"]
            table_matrix.append(row)

writer = MarkdownTableWriter(
    headers=["App", "Version", "Bypass", "Notes"],
    value_matrix=table_matrix,
    margin=1  # add a whitespace for both sides of each cell
)
writer.write_table()



