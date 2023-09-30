# UserDefinedPhraser
> Doc Version: 1.1.1-20200531

🇺🇸 English | [🇨🇳 简体中文](README-CN.md)

* Convert pre-defined User Defined Phrases(UDP) to supported format for Win10 Pinyin IME, macOS Pinyin IME (+iOS/iPadOS), QQPinyin. Also generate HTML and JSON file for further usage.

## Basics
* Based on the `.json` file as the input, convert to other formats.

## Usage

```py
# Quick Start
python3 run_parser.py
```

```sh
|-- Phrasers/  # Parser classes for decode from target format to python dict and encode python dict to target format.
    |-- phraser.py  # Base class for all the phraser classes.
    |-- jsonphraser.py  # Parse `.json` file.
    |-- macphraser.py  # Parse macOS `.plist` file.
    |-- msphraser.py  # Parse Win10 Pinyin IME `.dat` file.
    |-- txtphraser.py  # Parse QQPinyin `.ini` file.
    |-- htmlpharser.py  # Generate `.html` file.
    |-- htmlphraser_tpl.py  # Template for `.html` file generation.
|-- Phrases/  # User Defined Phrases in JSON format, as the input to conversions.
    |-- UDP-*.json  # User Defined Phrases in JSON format.
|-- GeneratedUDP/  # This Folder holds the generated files. You can delete these files any time, they are not important.
|-- user_defined_phraser.py  # Main entry of program. Convert `.json` or `.toml` files to other formats.
```

* All Python Dict and JSON format is: `{ 'phrase': "<PHRASE>", 'shortcut': "<SHORTCUT>" }`
* `*Phraser` classes include `to_file()`, `from_file()`, `to_format*()`, `from_format*()` functions. They are used for read/write files and read/write formatted strings.

************

# Microsoft Pinyin IME
## Operations
### Delete
1. System Settings → Time and Languages → Region and Languages → Chinese → Preferences → Microsoft Pinyin → Preferences
2. Lexicon and self-learning → Add or Edit User Defined Phrases → Clear

### Add
1. System Settings → Time and Languages → Region and Languages → Chinese → Preferences → Microsoft Pinyin → Preferences
2. Lexicon and self-learning → Add or Edit User Defined Phrases → Import
3. `UserDefinedPhrase.dat`

### Format
* File suffix: `.dat` or `.lex`.
* Use `mschxudp` for formatting. Update with system update.

### References
* [imewlconverter · Github](https://github.com/studyzy/imewlconverter/tree/V2.3)
* [mschxudp · Github](https://github.com/hhggit/mschxudp)

## File Example
```
# win10 1703
#           proto8                   unknown_X   version
# 00000000  6d 73 63 68 78 75 64 70  02 00 60 00 01 00 00 00  |mschxudp..`.....|
#           phrase_offset_start
#                       phrase_start phrase_end  phrase_count
# 00000010  40 00 00 00 48 00 00 00  98 00 00 00 02 00 00 00  |@...H...........|
#           timestamp
# 00000020  49 4e 06 59 00 00 00 00  00 00 00 00 00 00 00 00  |IN.Y............|
# 00000030  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
#                                                      candidate2
#           phrase_offsets[]         magic_X     phrase_offset2
# 00000040  00 00 00 00 24 00 00 00  10 00 10 00 18 00 06 06  |....$...........|
#           phrase_unknown8_X        pinyin
# 00000050  00 00 00 00 96 0a 99 20  61 00 61 00 61 00 00 00  |....... a.a.a...|
#           phrase                               magic_X
# 00000060  61 00 61 00 61 00 61 00  61 00 00 00 10 00 10 00  |a.a.a.a.a.......|
#                       phrase_unknown8_X
#                 candidate2
#           offset2                        pinyin
# 00000070  1a 00 07 06 00 00 00 00  a6 0a 99 20 62 00 62 00  |........... b.b.|
#                             phrase
# 00000080  62 00 62 00 00 00 62 00  62 00 62 00 62 00 62 00  |b.b...b.b.b.b.b.|
# 00000090  62 00 62 00 62 00 00 00                           |b.b.b...|
```

* `proto8`: `'mschxudp'`
* `phrase_offset_start + 4 * phrase_count == phrase_start`
* `phrase_start + phrase_offsets[N] == magic(0x00080008)`
* `pinyin&phrase`: utf16-le string
* `hanzi_offset = 8 + len(pinyin)`
* `phrase_offsets[N] + offset + len(phrase) == phrase_offsets[N+1]`
* `candidate2`: 1st byte represent the phrase position

************

# macOS Pinyin IME
## Operations
### Delete

1. System Preferences → Keyboard → Text
2. Select any, <kbd>⌘</kbd><kbd>A</kbd>, click <kbd>-</kbd> or <kbd>⌫</kbd>/<kbd>delete</kbd>

### Add
1. System Preferences → Keyboard → Text
2. Drag `*.plist` into the window (one by one).

* Existing phrases will not duplicated, it's smart.

### Format
* `.plist` file with `xml` format.


## File Example
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"><?xml version="1.0" ?>
<plist version="1.0">
    <array>
        <dict>
            <key>phrase</key>
            <string>[word]</string>
            <key>shortcut</key>
            <string>[spell]</string>
        </dict>
        <dict>
            <key>phrase</key>
            <string>[word]</string>
            <key>shortcut</key>
            <string>[spell]</string>
        </dict>
    </array>
</plist>
```

************

# QQ Pinyin
## Opertaions
### Delete
1. QQPinyin → Settings → Lexicon → User Defined Phrases::Settings
2. Multi-select: hold <kbd>Ctrl</kbd> + <kbd>Click</kbd>, one by one.
3. Click delete.

### Add
1. QQPinyin → Settings → Lexicon → User Defined Phrases::Settings
2. Click "Import", select `*.txt` file.

### Format
* `.txt` format

## File Example
```ini
[spell]=[position],[word]
[spell]=[position],[word]
```
