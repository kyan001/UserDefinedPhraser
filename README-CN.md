# UserDefinedPhraser
> Doc Version: 1.1.1-20200531

[🇺🇸 English](README.md) | 🇨🇳 简体中文

* 将预定义的用户自定义短语（UDP）转化为可被 Win10 微软拼音、macOS 拼音输入法（+iOS/iPadOS）、QQ 拼音等输入法使用的导入文件。还可以生成 HTML 用于查看和 JSON 文件用于进一步处理。

## 基础
* 程序以 `.json` 文件为基准，转化为其他格式。

## 使用方法

```py
# 快速开始
python3 user_defined_phraser.py
```

```sh
|-- Phrasers/  # 将目标格式解析为 python 字典，并将 python 字典转为目标格式。
    |-- phraser.py  # 所有 Phraser 类的基类
    |-- jsonphraser.py  # 负责 json 格式文件的解析。
    |-- tomlphraser.py  # 负责 toml 格式文件的解析。
    |-- macphraser.py  # 负责 macOS `.plist` 文件的解析。
    |-- msphraser.py  # 负责 Win10 拼音输入法 `.dat` 文件的解析。
    |-- txtphraser.py  # 负责 QQ 拼音 `.ini` 文件的解析。
    |-- htmlphraser.py  # 负责生成 `.html` 文件。
    |-- htmlphraser_tpl.py  # 负责为生成的 `.html` 文件提供模板
|-- Phrases/  # 用户定义的短语，这些文件是所有生成文件的根本。
    |-- UDP-*.json  # 仅当使用 .json 存储的 UDP 文件。
    |-- UDP-*.toml  # 仅当使用 .toml 存储的 UDP 文件。
|-- GeneratedUDP/  # 此目录存放生成的文件，里面的文件可以随时删除。
|-- user_defined_phraser.py  # 程序总入口，负责将 `.json` 或 `.toml` 的格式转为其他格式。
```

* 所有 Python Dict 和 JSON 的格式均为：`{ 'phrase': "<PHRASE>", 'shortcut': "<SHORTCUT>" }`
* `*Phraser` 类都包含了 `to_file()`，`from_file()`，`to_format*()`，`from_format*()` 几种函数。分别用于生成、读取文件，以及生成、读取对应格式的字符串。

************

# 微软拼音输入法
## 手动操作
### 删除
1. 系统设置 → 时间和语言 → 区域和语言 → 中文（中华人民共和国） → 选项 → 微软拼音 → 选项
2. 词库和自学习 → 添加或编辑自定义短语 → 清除

### 添加
1. 系统设置 → 时间和语言 → 区域和语言 → 中文（中华人民共和国） → 选项 → 微软拼音 → 选项
2. 词库和自学习 → 添加或编辑自定义短语 → 导入
3. `UserDefinedPhrase.dat`

### 格式
* 文件后缀：`.dat` 或 `.lex`。
* 使用 `mschxudp` 的自定义格式，随着系统版本更新也会更新。

### 参考工具
* [imewlconverter · Github](https://github.com/studyzy/imewlconverter/tree/V2.3)
* [mschxudp · Github](https://github.com/hhggit/mschxudp)

## 文件范例
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
* `candidate2`: 第一个字节代表短语在候选框位置

************

# macOS 输入法
## 手动操作
### 清空
1. 系统偏好设置 → 键盘 → 文本
2. 点中任意项，<kbd>⌘</kbd><kbd>A</kbd>，点 <kbd>-</kbd> 号或 <kbd>⌫</kbd>/<kbd>delete</kbd>

### 添加
1. 系统偏好设置 → 键盘 → 文本
2. 拖拽 `*.plist` 文件到“输入码/短语”那个窗口处（一个个的拖）。

* 已存在的重复项不会重复添加，会智能添加。

### 格式
* `.plist` 文件，`xml` 格式


## 文件范例
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"><?xml version="1.0" ?>
<plist version="1.0">
    <array>
        <dict>
            <key>phrase</key>
            <string>[文字]</string>
            <key>shortcut</key>
            <string>[拼写]</string>
        </dict>
        <dict>
            <key>phrase</key>
            <string>[文字]</string>
            <key>shortcut</key>
            <string>[拼写]</string>
        </dict>
    </array>
</plist>
```

************

# QQ 拼音输入法
## 手动操作
### 删除
1. QQ输入法 → 属性设置 → 词库 → 自定义短语::设置
2. 多选：按住 <kbd>Ctrl</kbd> + <kbd>点击</kbd>，一个一个点。
3. 然后点删除。

### 添加
1. QQ输入法 → 属性设置 → 词库 → 自定义短语::设置
2. 点 “导入”，选中某个 `*.txt` 文件。

### 格式
* `.txt` 文件

## 文件范例
```ini
[拼写]=[位置],[短语]
[拼写]=[位置],[短语]
```
