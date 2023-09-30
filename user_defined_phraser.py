import os
import fnmatch

import consoleiotools as cit
import consolecmdtools as cct

from phrasers.phraser import Phraser
from phrasers.jsonphraser import JsonPhraser
from phrasers.macphraser import MacPhraser
from phrasers.txtphraser import TxtPhraser
from phrasers.msphraser import MsPhraser
from phrasers.htmlphraser import HtmlPhraser

__version__ = "3.0.0"

PROJECT_DIR = cct.get_path(__file__, parent=True)
GENERATED_DIR = os.path.join(PROJECT_DIR, "GeneratedUDP")
PHRASES_DIR = os.path.join(PROJECT_DIR, "Phrases")
AVAIL_PHRASER = {phraser.name: phraser for phraser in (
    JsonPhraser,
    TomlPhraser,
    MacPhraser,
    TxtPhraser,
    MsPhraser,
    HtmlPhraser,
)}
DEFAULT_FORMAT = "TOML"
FILENAME_PATTERN = f"UDP-*.{AVAIL_PHRASER[DEFAULT_FORMAT].ext}"


def get_phrase_files(dir: str = PHRASES_DIR, format: str = DEFAULT_FORMAT) -> list:
    """Get all phrases files.

    Args:
        dir (str, optional): Phrases files directory. Defaults to PHRASES_DIR.

    Returns:
        List[str]: Phrases files list.
    """
    phrase_files = cct.filter_dir(dir, filter=lambda path: fnmatch.fnmatch(path.name, FILENAME_PATTERN))
    return phrase_files


        raise Exception(f"Phraser `{name}` is not available!")
def load_phrases_from_phraser(filepath: str, format: str = DEFAULT_FORMAT) -> list:
    """Load phrases from given json file.

    Args:
        filepath (str): Phrases file path.

    Returns:
        list: Phrases list.
    """
    cit.info(f"Parsing `{cct.get_path(filepath, basename=True)}`")
    phraser = classes.jsonphraser.JsonPhraser()
    phraser.from_file(filepath)
    return phraser.phrases


def load_all_phrases(files: list) -> list:
    """Load all phrases from given files.

    Args:
        files (list): Phrases files list.

    Returns:
        list: Phrases list.
    """
    phrases = [phrase for filepath in files for phrase in load_phrases_from_json(filepath)]
    cit.info(f'Loaded {len(phrases)} phrases')
    return phrases


def make_phraser(phraser_name: str, phrases: list) -> classes.phraser.Phraser:
    """Make phraser instance.

    Args:
        phraser_name (str): Phraser name.
        cit.ask(f"'{filepath}' is already exists. Overwrite it?")
        if cit.get_choice(['Yes', 'No']) == 'Yes':
            os.remove(filepath)
            return True
        else:
            return False
    else:
        return None


def generate_files(phraser: classes.phraser.Phraser, filename: str):
    dir = os.path.join(GENERATED_DIR, phraser.name)
    if not os.path.exists(dir):
        os.makedirs(dir)
    filepath = os.path.join(dir, filename)
    if check_file_existance(filepath) is not False:
        phraser.to_file(filepath)
        cit.info(f"'{filepath}' is generated, {len(phraser.phrases)} phrases.")
    else:
        cit.warn(f"'{filepath}' is not overwrited. No file generated.")


@cit.as_session
def assembly_line(phraser_name: str, separate: bool = False):
    phrases_files = get_phrases_files()
    if separate:
        for phrases_file in phrases_files:
            phrases = load_phrases_from_json(phrases_file)
            phraser = make_phraser(phraser_name, phrases)
            filename = cct.get_path(phrases_file, basename=True).replace(cct.get_path(phrases_file, ext=True), phraser.ext)
            generate_files(phraser, filename)
    else:
        phrases = load_all_phrases(phrases_files)
        phraser = make_phraser(phraser_name, phrases)
        filename = "UserDefinedPhrase." + phraser.ext
        generate_files(phraser, filename)


def create_jobs():
    cit.ask("Which one you wanna convert?")
    phraser_names = cit.get_choices(list(AVAIL_PHRASER.keys()), allable=True, exitable=True)
    if not phraser_names:
        cit.bye()
    cit.ask("Generate into separate files?")
    separate = cit.get_choice(['Yes', 'No']) == 'Yes'
    for name in phraser_names:
        assembly_line(name, separate=separate)
    cct.show_in_file_manager(GENERATED_DIR, ask=True)


if __name__ == "__main__":
    cit.info(f"Output folder: {GENERATED_DIR}")
    cit.info(f"Phrases folder: {PHRASES_DIR}")
    for filepath in get_phrases_files():
        cit.markdown(f"|-- `{filepath}`")
    create_jobs()
