import os
import functools

import consoleiotools as cit
from UDPTools.macuserphraser import MacUserPhraser
from UDPTools.msuserphraser import MsUserPhraser
from UDPTools.jsonuserphraser import JsonUserPhraser
from UDPTools.txtuserphraser import TxtUserPhraser
from UDPTools.htmluserphraser import HtmlUserPhraser

COMMANDS = []
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
GENERATED_DIR = os.path.join(PROJECT_DIR, "GeneratedUDP")
AVAIL_PHRASER = {
    'json': {
        'phraser': JsonUserPhraser,
        'output': 'UserDefinedPhraser.json',
    },
    'mac': {
        'phraser': MacUserPhraser,
        'output': "UserDefinedPhrase.plist",
    },
    'qq': {
        'phraser': TxtUserPhraser,
        'output': "QQPinyin.txt",
    },
    'win10': {
        'phraser': MsUserPhraser,
        'output': "UserDefinedPhrase.dat",
    },
    'html': {
        'phraser': HtmlUserPhraser,
        'output': "UserDefinedPhrase.html",
    },
}


def json_filenames() -> list:
    all_files = os.listdir(PROJECT_DIR)
    return [filename for filename in all_files if filename.startswith('UDP-') and filename.endswith('.json')]


def get_project_filepaths(filenames: list) -> list:
    return [os.path.join(PROJECT_DIR, fn) for fn in filenames]


def load_phrases_from_json(filename: str) -> list:
    jup = JsonUserPhraser()
    jup.from_file(filename)
    return jup.phrases


def load_all_phrases_from_json(files: tuple) -> list:
    phrases = []
    for fn in files:
        phrases += load_phrases_from_json(fn)
    cit.info('Loaded {} phrases'.format(len(phrases)))
    return phrases


def generate_UDP_file(UserPhraser, output: str, phrases: list):
    if not UserPhraser:
        raise Exception("UserPhraser must provided!")
    if not output:
        raise Exception("No output filename provided!")
    phraser = UserPhraser(phrases)
    filepath = os.path.join(GENERATED_DIR, output)
    if os.path.exists(filepath):
        cit.ask("'{}' is already exists. Overwrite it?".format(filepath))
        if cit.get_choice(['Yes', 'No']) == 'Yes':
            os.remove(filepath)
        else:
            cit.warn("Output is not overwrited. No file generated.")
            return
    phraser.to_file(filepath)
    cit.info("'{o}' is generated, {length} phrases.".format(o=output, length=len(phraser.phrases)))


if __name__ == "__main__":
    json_files = json_filenames()
    cit.info("JSON file list:\n{}".format("\n".join(json_files)))
    phrases = load_all_phrases_from_json(get_project_filepaths(json_files))
    cit.ask("Which one you wanna convert?")
    phrsr_key = cit.get_choice(list(AVAIL_PHRASER.keys()) + ['** ALL **'])
    if phrsr_key == '** ALL **':
        for key, phraser_set in AVAIL_PHRASER.items():
            cit.title("Generating {}".format(key))
            generate_UDP_file(UserPhraser=phraser_set['phraser'], output=phraser_set['output'], phrases=phrases)
            cit.end()
    else:
        phraser_set = AVAIL_PHRASER[phrsr_key]
        cit.title("Generating {}".format(phrsr_key))
        generate_UDP_file(UserPhraser=phraser_set['phraser'], output=phraser_set['output'], phrases=phrases)
        cit.end()
