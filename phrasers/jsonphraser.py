import os
import json

from . import phraser

""".json format:
[
    {
        shortcut: "shortcut 1",
        phrase: "phrase 1",
    },
    {
        shortcut: "shortcut 2",
        phrase: "phrase 2",
    }
]
"""


class JsonPhraser(phraser.Phraser):
    ext = 'json'
    name = 'JSON'

    def from_file(self, filepath: str):
        """ Read `.json` file into objects."""
        if not filepath:
            raise Exception("No filepath provided")
        with open(filepath, encoding='utf8') as f:
            json_str = f.read()
        self.from_json(json_str)

    def to_file(self, filepath: str):
        if not filepath:
            raise Exception("No filepath provided")
        if os.path.exists(filepath):
            raise Exception("File '{}' already exists!".format(filepath))
        with open(filepath, 'w', encoding='utf8') as f:
            f.write(self.to_json())

    def from_json(self, json_str: str):
        self.phrases = [{'phrase': item['phrase'], 'shortcut': item['shortcut']} for item in json.loads(json_str)]

    def to_json(self):
        json_obj = [{'shortcut': item['shortcut'], 'phrase': item['phrase']} for item in self.phrases]
        return json.dumps(json_obj, indent=4, ensure_ascii=False)
