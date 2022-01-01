import os
import re
import yaml
import requests
import time
from urllib.parse import urlparse

def get_lookup_url(app_store_link):
    path = urlparse(app_store_link).path.split('/')
    itunes_id = re.search(r'id([0-9]+)', path[-1]).group(1)
    region = path[1]

    return f"https://itunes.apple.com/{region}/lookup?id={itunes_id}"


__scriptdir = os.path.dirname(os.path.realpath(__file__))
apps_dir = os.path.join(__scriptdir, '..', 'manifests', 'apps')
apps_files = [os.path.join(apps_dir, f) for f in os.listdir(apps_dir) if os.path.isfile(os.path.join(apps_dir, f))]

for app_file in apps_files:
    with open(app_file, encoding='utf-8') as file:
        app = yaml.safe_load(file.read())

    if 'bundleId' in app and 'icon' in app:
        continue

    with open(app_file, encoding='utf-8', mode='w') as file:
        r = requests.get(get_lookup_url(app['uri'])).json()
        app_new = dict()
        app_new['name'] = app['name']
        app_new['bundleId'] = r['results'][0]['bundleId']
        app_new['uri'] = app['uri']
        app_new['icon'] = r['results'][0]['artworkUrl512']
        app_new['bypasses'] = app['bypasses']

        file.write(yaml.dump(app_new, default_flow_style=False, sort_keys=False))
        time.sleep(5)