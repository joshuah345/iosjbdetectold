import os
import yaml
import hmac
import hashlib

from flask import Flask, request
from flask_restful import Resource, Api, reqparse

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def return_results(list_of_dicts, query, threshold):
    query = query.lower()
    scores = []
    for index, item in enumerate(list_of_dicts):
        values = [item['name'].lower()]
        ratios = [fuzz.partial_ratio(str(query), str(value)) for value in values] # ensure both are in string
        scores.append({ "index": index, "score": max(ratios)})

    filtered_scores = [item for item in scores if item['score'] >= threshold]
    sorted_filtered_scores = sorted(filtered_scores, key = lambda k: k['score'], reverse=True)
    filtered_list_of_dicts = [ list_of_dicts[item["index"]] for item in sorted_filtered_scores ]
    return filtered_list_of_dicts


def init_db(manifests_dir):
    __scriptdir = os.path.dirname(os.path.realpath(__file__))
    bypasses_file = os.path.join(__scriptdir, manifests_dir, 'bypasses.yaml')
    apps_dir = os.path.join(__scriptdir, manifests_dir, 'apps')

    with open(bypasses_file, encoding='utf-8') as file:
        bypasses = yaml.safe_load(file)

    db_data = list()
    apps_files = [os.path.join(apps_dir, f) for f in os.listdir(apps_dir) if os.path.isfile(os.path.join(apps_dir, f))]
    for app_file in apps_files:
        with open(app_file, encoding='utf-8') as file:
            app = yaml.safe_load(file.read())
        db_data.append(app)
    return bypasses, db_data


class App(Resource):
    def __init__(self):
        self.bypasses, self.db = init_db(os.path.join('..', 'manifests'))

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('search', required=True)
        parser.add_argument('fields', required=False)

        args = parser.parse_args()
        search_results = return_results(self.db, args.search, 78)

        for index, res in enumerate(search_results):
            if res['bypasses']:
                detailed_bypass_info = list()
                downgrade_noted = False
                for bypass in res['bypasses']:
                    if 'name' in bypass:
                        notes_from_bypass = self.bypasses[bypass['name']]['notes'] \
                                            if 'notes' in self.bypasses[bypass['name']] \
                                            else ''
                        if 'guide' in self.bypasses[bypass['name']]:
                            bypass['guide'] = self.bypasses[bypass['name']]['guide']

                        bypass['repository'] = self.bypasses[bypass['name']]['repository'] \
                                            if 'repository' in self.bypasses[bypass['name']] \
                                            else None
                        if 'notes' in bypass:
                            bypass['notes'] = [notes_from_bypass, bypass['notes']]
                        elif notes_from_bypass:
                            bypass['notes'] = notes_from_bypass
                    detailed_bypass_info.append(bypass)
                search_results[index]['bypasses'] = detailed_bypass_info

        if search_results:
            return {'status': 'Successful', 'data': search_results}
        else:
            return {'status': 'Not Found'}


class GitHubWebhook(Resource):
    def __init__(self):
        self.webhook_secret = os.environ.get('GITHUB_WEBHOOK_SECRET')

    def post(self):
        signature = 'sha256=' + hmac.new(self.webhook_secret, request.data, hashlib.sha256).hexdigest()
        if hmac.compare_digest(signature, request.headers.get('X-Hub-Signature-256')):
            content = request.json
            if content['ref'] == 'refs/heads/main':
                os.system('git -C /var/www/jbdetectlist pull')
                os.system('sudo /bin/systemctl restart jbdetectapi')
        else:
            return "Signatures didn't match!", 500


app = Flask(__name__)
api = Api(app)
api.add_resource(App, '/app')
if 'GITHUB_WEBHOOK_SECRET' in os.environ.keys():
    api.add_resource(GitHubWebhook, '/gh-webhook')


if __name__ == '__main__':
    app.run()



