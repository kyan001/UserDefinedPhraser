import os
import functools

import consoleiotools as cit
from Phrasers.macphraser import MacPhraser
from Phrasers.msphraser import MsPhraser
from Phrasers.jsonphraser import JsonPhraser
from Phrasers.txtphraser import TxtPhraser
from Phrasers.htmlphraser import HtmlPhraser

COMMANDS = []
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
GENERATED_DIR = os.path.join(PROJECT_DIR, "GeneratedUDP")
PHRASES_DIR = os.path.join(PROJECT_DIR, "Phrases")
AVAIL_PHRASER = {
    'json': {
        'phraser': JsonPhraser,
        'output': 'Phrases.json',
    },
    'mac': {
        'phraser': MacPhraser,
        'output': "macOS_Phrases.plist",
    },
    'qq': {
        'phraser': TxtPhraser,
        'output': "QQPinyin_Phrases.txt",
    },
    'win10': {
        'phraser': MsPhraser,
        'output': "UserDefinedPhrase.dat",
    },
    'html': {
        'phraser': HtmlPhraser,
        'output': "Phrases.html",
    },
}


def phrases_filenames() -> list:
    phrases_files = os.listdir(PHRASES_DIR)
    return [filename for filename in phrases_files if filename.startswith('UDP-') and filename.endswith('.json')]


def load_all_phrases(files: tuple) -> list:
    def load_phrases_from_json(filename: str) -> list:
        cit.info("Parsing {}".format(filename))
        jup = JsonPhraser()
        jup.from_file(filename)
        return jup.phrases

    phrases = [phrase for filename in files for phrase in load_phrases_from_json(filename)]
    cit.info('Loaded {} phrases'.format(len(phrases)))
    return phrases


def generate_UDP_file(Phraser: object, output: str, phrases: list):
    if not Phraser:
        raise Exception("Phraser must provided!")
    if not output:
        raise Exception("No output filename provided!")
    phraser = Phraser(phrases)
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
    phrases_filenames = phrases_filenames()
    deco = "\n| * "
    cit.info("JSON file list:{deco}{data}".format(deco=deco, data=deco.join(phrases_filenames)))
    phrases_paths = [os.path.join(PHRASES_DIR, fn) for fn in phrases_filenames]
    phrases = load_all_phrases(phrases_paths)
    cit.ask("Which one you wanna convert?")
    phrsr_key = cit.get_choice(list(AVAIL_PHRASER.keys()) + ['** ALL **'])
    if phrsr_key == '** ALL **':
        for key, phraser_set in AVAIL_PHRASER.items():
            cit.title("Generating {}".format(key))
            generate_UDP_file(Phraser=phraser_set['phraser'], output=phraser_set['output'], phrases=phrases)
            cit.end()
    else:
        phraser_set = AVAIL_PHRASER[phrsr_key]
        cit.title("Generating {}".format(phrsr_key))
        generate_UDP_file(Phraser=phraser_set['phraser'], output=phraser_set['output'], phrases=phrases)
        cit.end()
