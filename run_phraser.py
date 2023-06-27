import os
import functools
import sys
import subprocess
import platform

import consoleiotools as cit
import consolecmdtools as cct

import classes.macphraser
import classes.msphraser
import classes.jsonphraser
import classes.txtphraser
import classes.htmlphraser

__version__ = "1.0.1"

COMMANDS = []
PROJECT_DIR = cct.get_dir(__file__)
GENERATED_DIR = os.path.join(PROJECT_DIR, "GeneratedUDP")
PHRASES_DIR = os.path.join(PROJECT_DIR, "Phrases")
AVAIL_PHRASER = {
    'JSON': classes.jsonphraser.JsonPhraser,
    'macOS': classes.macphraser.MacPhraser,
    'QQ': classes.txtphraser.TxtPhraser,
    'Windows': classes.txtphraser.MsPhraser,
    'HTML': classes.htmlphraser.HtmlPhraser,
}


def get_phrases_files(dir: str = PHRASES_DIR) -> list:
    """Get all phrases files.

    Args:
        dir (str, optional): Phrases files directory. Defaults to PHRASES_DIR.

    Returns:
        List[str]: Phrases files list.
    """
    phrases_files = os.listdir(dir)
    return [os.path.join(dir, filename) for filename in phrases_files if filename.startswith('UDP-') and filename.endswith('.json')]


def load_phrases_from_json(filepath: str) -> list:
    """Load phrases from given json file.

    Args:
        filepath (str): Phrases file path.

    Returns:
        list: Phrases list.
    """
    cit.info(f"Parsing `{cct.get_dir(filepath, mode='basename')}`")
    jup = classes.jsonphraser.JsonPhraser()
    jup.from_file(filepath)
    return jup.phrases


@cit.as_session
def load_all_phrases(files: list) -> list:
    """Load all phrases from given files.

    Args:
        files (list): Phrases files list.

    Returns:
        list: Phrases list.
    """
    phrases = [phrase for filepath in files for phrase in load_phrases_from_json(filepath)]
    cit.info('Loaded {} phrases'.format(len(phrases)))
    return phrases


def generate_file_from_phrases(phrases: list, phraser_name: str, separate: bool = False):
    """Generate UDP file using given phraser and phrases.

    Args:
        phrases (list): Phrases list.
        out_path (str): Output file path.
        phraser (str): Phraser name.
        separate (bool, optional): Generate all phrases into one file. Defaults to False.

    Raises:
        Exception:
    """
    if not phrases:
        raise Exception("No phrases provided!")
    if not phraser_name:
        raise Exception("No phraser provided!")
    if not out_path:
        raise Exception("No output path provided!")
    if phraser_name not in AVAIL_PHRASER:
        raise Exception(f"Phraser '{phraser_name}' is not available!")
    Phraser = AVAIL_PHRASER[phraser_name]
    phraser = Phraser(phrases)
    # os.path.join(GENERATED_DIR, phraselet['folder'], phraselet['name'])
    # if separate
    #
    if separate:
        for phrases_file in get_phrases_files():
            phrases = load_phrases_from_json(phrases_file)
            out_path = os.path.join(GENERATED_DIR, phraser_name, phrases_file)
    else:
        phrases = load_all_phrases()
        filename = UserDefinedPhrase

def generate_UDP_file(Phraser: object, output_filename: str, phrases: list):
    if not Phraser:
        raise Exception("Phraser must provided!")
    if not output_filename:
        raise Exception("No output filename provided!")
    phraser = Phraser(phrases)
    filepath = os.path.join(GENERATED_DIR, output_filename)
    if os.path.exists(filepath):
        cit.ask("'{}' is already exists. Overwrite it?".format(filepath))
        if cit.get_choice(['Yes', 'No']) == 'Yes':
            os.remove(filepath)
        else:
            cit.warn("output_filename is not overwrited. No file generated.")
            return
    phraser.to_file(filepath)
    cit.info("'{o}' is generated, {length} phrases.".format(o=output_filename, length=len(phraser.phrases)))


if __name__ == "__main__":
    cit.info("Output Folder: {}".format(GENERATED_DIR))
    cit.info("Phrases File location: {}".format(PHRASES_DIR))
    deco = "\n| * "
    phrases_filenames =
    cit.info("Phrases JSON Files:")
    cit.markdown("\n".join([f"* `{filename}`" for filename in phrases_filenames]))
    phrases_paths = [os.path.join(PHRASES_DIR, fn) for fn in phrases_filenames]
    phrases = load_all_phrases(phrases_paths)
    cit.ask("Which one you wanna convert?")
    phrsr_keys = cit.get_choices(list(AVAIL_PHRASER.keys()), allable=True, exitable=True)
    if not phrsr_keys:
        cit.bye()
    for key in phrsr_keys:
        cit.title("Generating {}".format(key))
        phraselet = AVAIL_PHRASER[key]
        out_filepath =
        generate_UDP_file(Phraser=phraselet['phraser'], filepath=out_filepath, phrases=phrases)
        cit.end()
    cct.show_in_folder(GENERATED_DIR, ask=True)
