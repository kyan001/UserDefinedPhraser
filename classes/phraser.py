class Phraser:
    ext = ''  # filename extension
    name = ''  # phraser name

    def __init__(self, phrases: list = []):
        self.phrases = phrases  # save all the "phrase & shortcut".

    def __str__(self):
        return str(self.phrases)

    def __list__(self):
        return self.phrases
