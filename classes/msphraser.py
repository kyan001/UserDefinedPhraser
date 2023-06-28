import os
from io import SEEK_SET
import tempfile
import struct
from datetime import datetime

from . import phraser

# win10 1703
#           proto8                   unknown_X   version
# 00000000  6d 73 63 68 78 75 64 70  02 00 60 00 01 00 00 00  |mschxudp..`.....|
#           phrase_offset_start
#                       phrase_start phrase_end  phrase_count
# 00000010  40 00 00 00 48 00 00 00  98 00 00 00 02 00 00 00  |@...H...........|
#           timestamp
# 00000020  49 4e 06 59 00 00 00 00  00 00 00 00 00 00 00 00  |IN.Y............|
# 00000030  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
#                                                      frequency
#           phrase_offsets[]         magic_X     phrase_offset2
# 00000040  00 00 00 00 24 00 00 00  10 00 10 00 18 00 06 06  |....$...........|
#           phrase_unknown8_X        pinyin
# 00000050  00 00 00 00 96 0a 99 20  61 00 61 00 61 00 00 00  |....... a.a.a...|
#           phrase                               magic_X
# 00000060  61 00 61 00 61 00 61 00  61 00 00 00 10 00 10 00  |a.a.a.a.a.......|
#                       phrase_unknown8_X
#                 frequency
#           offset2                        pinyin
# 00000070  1a 00 07 06 00 00 00 00  a6 0a 99 20 62 00 62 00  |........... b.b.|
#                             phrase
# 00000080  62 00 62 00 00 00 62 00  62 00 62 00 62 00 62 00  |b.b...b.b.b.b.b.|
# 00000090  62 00 62 00 62 00 00 00                           |b.b.b...|
# 00000098


# win10 1607
#           proto8                   version     phrase_offset_start
# 00000000  6d 73 63 68 78 75 64 70  01 00 00 00 40 00 00 00  |mschxudp....@...|
#          phrase_start phrase_end   phrase_count unknown_X
# 00000010  48 00 00 00 7e 00 00 00  02 00 00 00 00 00 00 00  |H...~...........|
#           timestamp
# 00000020  29 b8 cc 58 00 00 00 00  00 00 00 00 00 00 00 00  |)..X............|
# 00000030  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
#                                                      frequency
#           phrase_offsets[]         magic       offset2
# 00000040  00 00 00 00 1c 00 00 00  08 00 08 00 10 00 01 06  |................|
#           pinyin                   phrase
# 00000050  61 00 61 00 61 00 00 00  61 00 61 00 61 00 61 00  |a.a.a...a.a.a.a.|
#                                                pinyin
#                                          frequency
#                       magic        offset2
# 00000060  61 00 00 00 08 00 08 00  10 00 05 06 62 00 62 00  |a...........b.b.|
#                       phrase
# 00000070  62 00 00 00 62 00 62 00  62 00 62 00 00 00        |b...b.b.b.b...|
# 0000007e


class MsPhraser(phraser.Phraser):
    ext = 'dat'
    name = 'Windows'

    def from_file(self, filepath: str):
        if not filepath:
            raise Exception("No filepath provided")
        with open(filepath, 'rb', encoding='utf8') as fl:
            dat_str = fl.read()
        self.from_dat(dat_str)

    def to_file(self, filepath: str):
        if not filepath:
            raise Exception("No filepath provided")
        if os.path.exists(filepath):
            raise Exception("File '{}' already exists!".format(filepath))
        mfb = MschxudpBuilder()
        for itm in self.phrases:
            mfb.add_phrase(shortcut=itm['shortcut'], phrase=itm['phrase'])
        mfb.save(filepath)

    def from_dat(self, dat_str: str):
        pass  # TODO

    def to_dat(self):
        dat_str = ""
        with tempfile.TemporaryDirectory() as dir:
            filepath = os.path.join(dir, "UserDefinedPhrase.dat")
            self.to_file(filepath)
            with open(filepath, 'rb', encoding='utf8') as fl:
                dat_str = fl.read()
        return dat_str


class MschxudpBuilder(object):
    def __init__(self, win10='1703', phrase_magic=0x00100010):
        self.phrases = []
        self.proto = b'mschxudp'
        self.version = 1
        self.phrase_offset_start = 0x00000040
        if win10 == '1703' or phrase_magic == 0x00100010:
            self.unknown = 0x00600002
            self.phrase_magic = 0x00100010
            self.phrase_unknown = 0x20990A9600000000
        elif win10 == '1607' or phrase_magic == 0x00080008:
            self.unknown = 0x00000000
            self.phrase_magic = 0x00080008
        else:
            raise Exception("Version Error: unsupported version {}".format(phrase_magic))

    def add_phrase(self, shortcut: str, phrase: str, candidate: int = 1, frequency: int = 6):
        if self.phrases and shortcut == self.phrases[-1]["shortcut"]:
            candidate = self.phrases[-1]["candidate"] + 1
        self.phrases.append({
            "shortcut": shortcut,
            "phrase": phrase,
            "candidate": candidate,
            "frequency": frequency,
        })

    def save(self, file_name):
        with open(file_name, 'wb') as fl:
            phrase_count = len(self.phrases)
            phrase_start = self.phrase_offset_start + phrase_count * 4

            fl.seek(phrase_start, SEEK_SET)

            phrase_offsets = []
            phrase_offset = 0
            for itm in self.phrases:
                phrase_offsets.append(phrase_offset)
                shortcut_utf16 = (itm['shortcut'] + '\0').encode('utf-16-le')
                phrase_utf16 = (itm['phrase'] + '\0').encode('utf-16-le')
                if self.phrase_magic == 0x00100010:
                    offset = 0x0010 + len(shortcut_utf16)
                    fl.write(struct.pack('IHBBQ', self.phrase_magic, offset, itm['candidate'], itm['frequency'], self.phrase_unknown))
                elif self.phrase_magic == 0x00080008:
                    offset = 0x0008 + len(shortcut_utf16)
                    fl.write(struct.pack('IHBB', self.phrase_magic, offset, itm['candidate'], itm['frequency']))
                else:
                    raise Exception("Version Error: unsupported version {}".format(self.phrase_magic))
                fl.write(shortcut_utf16)
                fl.write(phrase_utf16)
                phrase_offset += offset + len(phrase_utf16)

            phrase_end = phrase_start + phrase_offset
            timestamp = int(datetime.now().timestamp())

            fl.seek(0, SEEK_SET)
            fl.write(self.proto)
            assert fl.tell() == 8

            if self.phrase_magic == 0x00100010:
                fl.write(struct.pack('IIIIIII', self.unknown, self.version, self.phrase_offset_start, phrase_start, phrase_end, phrase_count, timestamp))
            elif self.phrase_magic == 0x00080008:
                fl.write(struct.pack('IIIIIII', self.version, self.phrase_offset_start, phrase_start, phrase_end, phrase_count, self.unknown, timestamp))
            else:
                raise Exception("Version Error: unsupported version {}".format(self.phrase_magic))
            assert fl.tell() == 0x24

            fl.seek(self.phrase_offset_start, SEEK_SET)
            for i in phrase_offsets:
                fl.write(struct.pack('i', i))
