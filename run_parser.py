import os
import functools
import sys
import subprocess
import platform

import consoleiotools as cit
import consolecmdtools as cct

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


def get_phrases_filenames() -> list:
    phrases_files = os.listdir(PHRASES_DIR)
    return [filename for filename in phrases_files if filename.startswith('UDP-') and filename.endswith('.json')]


@cit.as_session
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
    cit.info("Output Folder: {}".format(GENERATED_DIR))
    cit.info("Phrases File location: {}".format(PHRASES_DIR))
    deco = "\n| * "
    phrases_filenames = get_phrases_filenames()
    cit.info("Phrases JSON Files:")
    for filename in phrases_filenames:
        cit.echo(filename, pre="*")
    phrases_paths = [os.path.join(PHRASES_DIR, fn) for fn in phrases_filenames]
    phrases = load_all_phrases(phrases_paths)
    cit.ask("Which one you wanna convert?")
    phrsr_keys = cit.get_choices(list(AVAIL_PHRASER.keys()), allable=True, exitable=True)
    if not phrsr_keys:
        cit.bye()
    for key in phrsr_keys:
        cit.title("Generating {}".format(key))
        phraselet = AVAIL_PHRASER[key]
        generate_UDP_file(Phraser=phraselet['phraser'], output=phraselet['output'], phrases=phrases)
        cit.end()
    cct.show_in_folder(GENERATED_DIR, ask=True)
