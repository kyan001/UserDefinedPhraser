import os

from bs4 import BeautifulSoup
from bs4 import Doctype


class MacUserPhraser:
    def __init__(self, phrases: list = []):
        self.phrases = phrases  # save all the "phrase & shortcut".

    def __str__(self):
        return str(self.phrases)

    def __list__(self):
        return self.phrases

    def from_file(self, filepath: str):
        """ Read file into objects."""
        if not filepath:
            raise Exception("No filepath provided")
        with open(filepath, encoding='utf8') as f:
            plist_str = f.read()
        self.from_plist(plist_str)

    def to_file(self, filepath: str):
        if not filepath:
            raise Exception("No filepath provided")
        if os.path.exists(filepath):
            raise Exception("File '{}' already exists!".format(filepath))
        with open(filepath, 'w', encoding='utf8') as f:
            f.write(self.to_plist())

    def from_plist(self, plist_str: str):
        soup = BeautifulSoup(plist_str, 'xml')
        for dct in soup.find_all('dict'):
            phrase = dct.find_all('string')[0].string
            shortcut = dct.find_all('string')[1].string
            self.phrases.append({'phrase': phrase, 'shortcut': shortcut})

    def to_plist(self):
        def prettify(soup):
            return str(soup).replace("<array>", "\n    <array>").replace("<dict>", "\n        <dict>").replace("<key>", "\n            <key>").replace("<string>", "\n            <string>").replace("</dict>", "\n        </dict>").replace("</array>", "\n    </array>").replace("</plist>", "\n</plist>")
        soup = BeautifulSoup('', 'xml')
        doctype = Doctype('plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"')
        soup.append(doctype)
        soup.append(soup.new_tag('plist', version="1.0"))
        soup.plist.append(soup.new_tag('array'))
        for itm in self.phrases:
            dct = soup.new_tag('dict')
            phrase_key = soup.new_tag('key')
            phrase_key.string = "phrase"
            phrase_string = soup.new_tag('string')
            phrase_string.string = itm['phrase']
            shortcut_key = soup.new_tag('key')
            shortcut_key.string = "shortcut"
            shortcut_string = soup.new_tag('string')
            shortcut_string.string = itm['shortcut']
            dct.append(phrase_key)
            dct.append(phrase_string)
            dct.append(shortcut_key)
            dct.append(shortcut_string)
            soup.array.append(dct)
        return prettify(soup)
