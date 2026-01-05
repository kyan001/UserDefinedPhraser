class Phraser:
    ext = ''  # filename extension
    name = ''  # phraser name

    def __init__(self, phrases: list | None = None):  # cannot use [] as default value, it will be shared between instances.
        self.phrases = phrases or []  # save all the "phrase & shortcut".

    def __str__(self):
        return str(self.phrases)

    def __list__(self):
        return self.phrases

    def to_file(self, filepath: str):
        raise NotImplementedError
