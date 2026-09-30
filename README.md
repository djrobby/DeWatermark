# DeWatermark

**The AI text fingerprint and watermark remover for Sublime Text.**

DeWatermark instantly cleans pasted AI-generated text by removing hidden Unicode characters, suspicious text markers, homoglyphs, unusual whitespace, and typography artifacts that can act as fingerprints in generated or copied text.

Paste through DeWatermark and get back clean, normalized text.

## Remove AI Watermarks Instantly

AI-generated and web-copied text can contain invisible or unusual Unicode characters that you would never notice by looking at the document.

DeWatermark inspects your clipboard character-by-character before inserting it into Sublime Text and removes or normalizes known text artifacts.

It works entirely locally, requires no external services, and does not send your text anywhere.

## What AI Text Watermarks Are

Text can contain characters and formatting that are completely or nearly invisible to the reader but remain embedded in the underlying Unicode.

Common examples include:

- **Hidden Unicode Characters** - Zero-width spaces, zero-width joiners, word joiners, BOM characters, and other invisible characters.
- **Directional Formatting** - Left-to-right and right-to-left marks, embeddings, overrides, and Unicode isolate characters.
- **Homoglyphs** - Cyrillic or Greek characters that visually resemble ordinary Latin letters but have completely different Unicode code points.
- **Unusual Whitespace** - Non-breaking spaces, narrow no-break spaces, figure spaces, and other Unicode whitespace.
- **Typography Fingerprints** - Smart quotes, em dashes, en dashes, Unicode ellipses, and similar typography that can distinguish copied/generated text from plain text.
- **Explicit Markers** - Known unwanted Unicode characters or marker sequences that can be removed before text is inserted.

DeWatermark converts these artifacts into predictable, ordinary text.

## What DeWatermark Removes

DeWatermark currently detects and removes invisible characters including:

```text
U+200B  ZERO WIDTH SPACE
U+200C  ZERO WIDTH NON-JOINER
U+200D  ZERO WIDTH JOINER
U+2060  WORD JOINER
U+FEFF  ZERO WIDTH NO-BREAK SPACE / BOM
U+200E  LEFT-TO-RIGHT MARK
U+200F  RIGHT-TO-LEFT MARK
U+202A  LEFT-TO-RIGHT EMBEDDING
U+202B  RIGHT-TO-LEFT EMBEDDING
U+202C  POP DIRECTIONAL FORMATTING
U+202D  LEFT-TO-RIGHT OVERRIDE
U+202E  RIGHT-TO-LEFT OVERRIDE
U+2066  LEFT-TO-RIGHT ISOLATE
U+2067  RIGHT-TO-LEFT ISOLATE
U+2068  FIRST STRONG ISOLATE
U+2069  POP DIRECTIONAL ISOLATE
```

## Homoglyph Detection

Some Unicode characters look virtually identical to ordinary ASCII characters.

For example, Cyrillic:

```text
а е о р с х у і ѕ ј
```

can visually resemble:

```text
a e o p c x y i s j
```

DeWatermark detects supported homoglyphs and converts them to their normal Latin equivalents.

Selected Greek homoglyphs are handled as well.

## Typography Normalization

DeWatermark converts common Unicode typography into predictable ASCII equivalents.

For example:

```text
Curly single quotes  -> '
Curly double quotes  -> "
En dash              -> -
Em dash              -> -
Ellipsis              -> ...
Non-breaking space   -> SPACE
Narrow no-break space -> SPACE
Figure space         -> SPACE
```

This leaves you with clean, portable plain text.

## One-Step Clean Paste

DeWatermark is designed to be simple.

Copy your text normally, then open the Sublime Text Command Palette:

```text
Ctrl+Shift+P
```

and select:

```text
DeWatermark: Paste Clean
```

DeWatermark:

1. Reads your clipboard.
2. Scans every character.
3. Removes configured invisible characters and markers.
4. Converts supported homoglyphs.
5. Normalizes typography and unusual whitespace.
6. Pastes the cleaned text into Sublime Text.
7. Reports exactly what it changed.

## Keyboard Shortcut

You can make DeWatermark your clean-paste shortcut:

```json
[
    {
        "keys": ["ctrl+shift+v"],
        "command": "dewatermark_paste"
    }
]
```

Add the binding through:

```text
Preferences -> Key Bindings
```

Now `Ctrl+Shift+V` becomes your AI-cleaning paste command.

## See Exactly What Was Removed

DeWatermark doesn't silently modify your clipboard text without explanation.

Every operation produces a detailed report in the Sublime Text console.

Example:

```text
======================================================================
DeWatermark
======================================================================
CLEANED - 1250 -> 1246 chars

Summary:
  Removed:  4
  Replaced: 7

REMOVED:
  4x  U+200B ZERO WIDTH SPACE  '\u200b'

REPLACED:
  3x  U+2019 RIGHT SINGLE QUOTATION MARK  '’' -> "'"  [TYPOGRAPHY]
  4x  U+2014 EM DASH  '—' -> '-'  [TYPOGRAPHY]

======================================================================
```

If nothing is found:

```text
DeWatermark: Clean - no watermarks detected.
```

## Private by Design

DeWatermark runs entirely inside Sublime Text.

- No APIs
- No accounts
- No telemetry
- No network requests
- No external AI models
- No text uploaded anywhere

Your clipboard contents stay on your computer.

## Important Note

DeWatermark removes detectable Unicode artifacts, homoglyphs, formatting characters, markers, and typography covered by its cleanup rules.

It does **not** claim to determine whether text was written by AI, defeat every AI-detection system, or remove statistical patterns based on writing style. Systems that analyze vocabulary, sentence structure, token probabilities, or other linguistic characteristics operate independently of the Unicode artifacts DeWatermark removes.

DeWatermark is deterministic - if an unwanted character is present and covered by a rule, it is removed or normalized.

## Installation

### Package Control

1. Open the Command Palette with `Ctrl+Shift+P`
2. Select `Package Control: Install Package`
3. Search for `DeWatermark`
4. Press Enter

### Manual Installation

Clone this repository into your Sublime Text `Packages` directory:

```bash
git clone https://github.com/djrobby/DeWatermark.git
```

Restart Sublime Text if necessary.

## Requirements

- Sublime Text 3 or newer
- No external Python dependencies

## License

DeWatermark is released under the MIT License.

See [LICENSE](LICENSE) for details.
