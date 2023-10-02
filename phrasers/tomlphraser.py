import os

import tomlkit

from . import phraser

""".toml format:
[[phrases]]
"shortcut 1" = "phrase 1"

[[phrases]]
"shortcut 2" = "phrase 2"
"""


class TomlPhraser(phraser.Phraser):
    ext = "toml"
    name = "TOML"

    def from_file(self, filepath: str):
        """ Read `.toml` file into objects."""
        if not filepath:
            raise Exception("No filepath provided")
        with open(filepath, encoding="utf8") as f:
            toml_str = f.read()
        self.from_toml(toml_str)

    def to_file(self, filepath: str):
        if not filepath:
            raise Exception("No filepath provided")
        if os.path.exists(filepath):
            raise Exception("File `{}` already exists!".format(filepath))
        with open(filepath, "w", encoding="utf8") as f:
            f.write(self.to_toml())

    def from_toml(self, toml_str: str):
        for phrase in tomlkit.loads(toml_str).get("phrases"):
            for k, v in phrase.items():  # k is `str`, v is `tomlkit.items.String`
                self.phrases.append({"shortcut": str(k), "phrase": str(v)})

    def to_toml(self):
        toml_obj = {"phrases": [{item['shortcut']: item['phrase']} for item in self.phrases]}
        return tomlkit.dumps(toml_obj)
