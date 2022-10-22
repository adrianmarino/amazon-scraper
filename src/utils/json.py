import json

def save_json(path, data):
    with open(f'{path}.json', 'w') as outfile:
        outfile.write(json.dumps(data, indent=2))
