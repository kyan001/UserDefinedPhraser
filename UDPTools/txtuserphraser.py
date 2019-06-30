import os


class TxtUserPhraser:
    def __init__(self, phrases: list = []):
        self.phrases = phrases

    def __str__(self):
        return str(self.phrases)

    def __list__(self):
        return self.phrases

    def from_file(self, filepath: str):
        if not filepath:
            raise Exception("No filepath provided")
        with open(filepath, encoding='utf8') as f:
            txt_str = f.read()
        self.from_txt(txt_str)

    def to_file(self, filepath: str):
        if not filepath:
            raise Exception("No filepath provided")
        if os.path.exists(filepath):
            raise Exception("File '{}' already exists!".format(filepath))
        with open(filepath, 'w', encoding='utf8') as f:
            f.write(self.to_txt())

    def from_txt(self, txt_str: str, separators="=1,"):
        for line in txt_str.split('\n'):
            shortcut, phrase = line.split(separators)
            self.phrases.append({'phrase': phrase, 'shortcut': shortcut})

    def to_txt(self, fmt: str = '{shortcut}=1,{phrase}'):
        return "\n".join([fmt.format(shortcut=itm['shortcut'], phrase=itm['phrase']) for itm in self.phrases])
