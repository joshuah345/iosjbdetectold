import os
import yaml
import logging
import argparse
from pytablewriter import MarkdownTableWriter


def markdown_link(name, uri, sharerepo=False):
    sharerepo_site = "https://sharerepo.stkc.win/?repo="
    return f"[{name}]({sharerepo_site}{uri})" if sharerepo else f"[{name}]({uri})"


def main():
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
    appstorepp_repo = 'https://cokepokes.github.io'

    with open(bypasses_file, encoding='utf-8') as file:
        bypasses = yaml.safe_load(file)

    # List all files in manifests/apps
    table_matrix = list()
    apps_files = [os.path.join(apps_dir, f) for f in os.listdir(apps_dir) if os.path.isfile(os.path.join(apps_dir, f))]
    for app_file in apps_files:
        with open(app_file, encoding='utf-8') as file:
            app = yaml.safe_load(file.read())

        app_name = markdown_link(app['name'], app['uri'])        
        bypass_versions = list()
        bypass_tweaks = list()
        bypass_notes = list()
        downgrade_noted = False
        if app['bypasses'] is None:
            bypass_versions.append('')
            bypass_tweaks.append('No known bypass')
            bypass_notes.append('')
        else:
            for bypass in app['bypasses']:
                bypass_versions.append(f"{bypass['version']}" if 'version' in bypass else '')

                if 'name' in bypass:
                    bypass_tweak = f"{markdown_link(bypass['name'], bypasses[bypass['name']]['guide'])}" \
                                        if 'guide' in bypasses[bypass['name']] \
                                        else bypass['name']
                    bypass_tweak_repo = f" ({markdown_link('repo', bypasses[bypass['name']]['repo'], sharerepo=True)})" \
                                            if 'repo' in bypasses[bypass['name']] \
                                            else ''
                    bypass_tweaks.append(bypass_tweak + bypass_tweak_repo)

                    if not downgrade_noted and 'version' in bypass and bypass['name'] != "AppStore++":
                        bypass_notes.append(
                            f"- Use AppStore++ ({markdown_link('repo', appstorepp_repo, sharerepo=True)}) to downgrade.")
                        downgrade_noted = True

                    notes_from_bypass = f"{bypasses[bypass['name']]['notes']} " \
                                            if 'notes' in bypasses[bypass['name']] \
                                            else ''
                    notes_from_manifest = bypass['notes'] \
                                            if 'notes' in bypass \
                                            else ''
                    if notes_from_bypass or notes_from_manifest:
                        bypass_notes.append(f"- **{bypass['name']}**: " + notes_from_bypass + notes_from_manifest)
                elif 'notes' in bypass:
                    logger.warning('Bypass name not specified, printing notes only')
                    bypass_notes.append(f"- {bypass['notes']}")
                else: 
                    logger.error('Neither name nor notes were supplied for this bypass!')
                    continue  
        table_matrix.append([f"{app_name}", '<br>'.join(bypass_versions),
                             '<br>'.join(bypass_tweaks), '<br>'.join(bypass_notes)])

    table_matrix.sort(key=lambda a: a[0].lower())
    writer = MarkdownTableWriter(
        headers=["App", "Version", "Bypass", "Notes"],
        value_matrix=table_matrix,
        margin=1  # add a whitespace for both sides of each cell
    )

    # Writing to the actual app-list.md
    if args.print:
        writer.write_table()
    else:
        headers_dir = os.path.join(__scriptdir, 'md-headers')
        app_list_md = os.path.join(__scriptdir, '..', 'app-list.md')
        with open(os.path.join(headers_dir, 'app-list.md'), encoding='utf-8', mode='r') as infile, \
                open(app_list_md, encoding='utf-8', mode='w') as outfile:
            outfile.write(infile.read())
            outfile.write('\n\n')
            outfile.write(writer.dumps())


if __name__ == "__main__":
    main()
