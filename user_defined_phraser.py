#! .venv/bin/python
import os
import fnmatch

import consoleiotools as cit
import consolecmdtools as cct

from phrasers.phraser import Phraser
from phrasers.jsonphraser import JsonPhraser
from phrasers.tomlphraser import TomlPhraser
from phrasers.macphraser import MacPhraser
from phrasers.txtphraser import TxtPhraser
from phrasers.msphraser import MsPhraser
from phrasers.htmlphraser import HtmlPhraser

__version__ = "3.0.2"

PROJECT_DIR = cct.get_path(__file__).parent
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
    phrase_files = cct.get_paths(dir, filter=lambda path: fnmatch.fnmatch(path.name, FILENAME_PATTERN))
    return phrase_files


def get_phraser(name: str = DEFAULT_FORMAT, phrases: list = []) -> Phraser:
    """Get phraser instance.

    Args:
        name (str, optional): Phraser name. Defaults to DEFAULT_FORMAT.
        phrases (list, optional): Phrases list. Defaults to [].

    Returns:
        Phraser: Phraser instance.
    """
    if name not in AVAIL_PHRASER:
        raise Exception(f"Phraser `{name}` is not available!")
    return AVAIL_PHRASER[name](phrases)


def load_phrases_from_phraser(filepath: str, format: str = DEFAULT_FORMAT) -> list:
    """Load phrases from given json file.

    Args:
        filepath (str): Phrases file path.

    Returns:
        list: Phrases list.
    """
    cit.info(f"Parsing `{cct.get_path(filepath).basename}`")
    phraser = AVAIL_PHRASER[format]()
    phraser.from_file(filepath)
    return phraser.phrases


def load_all_phrases(files: list) -> list:
    """Load all phrases from given files.

    Args:
        files (list): Phrases files list.

    Returns:
        list: Phrases list.
    """
    phrases = [phrase for filepath in files for phrase in load_phrases_from_phraser(filepath)]
    cit.info(f'Loaded {len(phrases)} phrases')
    return phrases


def generate_files(phraser: Phraser, filename: str):
    """Generate phrases file."""
    def check_file_existance(filepath: str):
        """Check if file exists, and ask user to overwrite it or not."""
        if os.path.exists(filepath):
            cit.ask(f"'{filepath}' is already exists. Overwrite it?")
            if cit.get_choice(['Yes', 'No']) == 'Yes':
                os.remove(filepath)
                return True
            else:
                return False
        else:
            return None

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
    phrases_files = get_phrase_files()
    if separate:
        for phrases_file in phrases_files:
            phrases = load_phrases_from_phraser(phrases_file)
            phraser = get_phraser(phraser_name, phrases)
            filename = f"{cct.get_path(phrases_file).stem}.{phraser.ext}"
            generate_files(phraser, filename)
    else:
        phrases = load_all_phrases(phrases_files)
        phraser = get_phraser(phraser_name, phrases)
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
    phrase_files = get_phrase_files()
    cit.info(f"Phrases files: {len(phrase_files)}")
    cct.ls_tree(PHRASES_DIR, to_visible=lambda path: fnmatch.fnmatch(path.name, FILENAME_PATTERN))
    create_jobs()
    cit.pause()
