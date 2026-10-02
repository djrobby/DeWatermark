import sublime
import sublime_plugin
import unicodedata
from collections import Counter


# ============================================================
# DeWatermark Rules
# ============================================================

INVISIBLE_CHARS = {
    '\u200B',  # Zero-width space
    '\u200C',  # Zero-width non-joiner
    '\u200D',  # Zero-width joiner
    '\u2060',  # Word joiner
    '\uFEFF',  # Zero-width no-break space / BOM
    '\u200E',  # Left-to-right mark
    '\u200F',  # Right-to-left mark
    '\u202A',  # Left-to-right embedding
    '\u202B',  # Right-to-left embedding
    '\u202C',  # Pop directional formatting
    '\u202D',  # Left-to-right override
    '\u202E',  # Right-to-left override
    '\u2066',  # Left-to-right isolate
    '\u2067',  # Right-to-left isolate
    '\u2068',  # First strong isolate
    '\u2069',  # Pop directional isolate
}

HOMOGLYPH_MAP = {
    # Cyrillic
    'а': 'a',
    'е': 'e',
    'о': 'o',
    'р': 'p',
    'с': 'c',
    'х': 'x',
    'у': 'y',
    'і': 'i',
    'ѕ': 's',
    'ј': 'j',

    # Greek
    'Α': 'A',
    'Β': 'B',
    'Ε': 'E',
    'Ζ': 'Z',
    'Η': 'H',
    'Ι': 'I',
    'Κ': 'K',
    'Μ': 'M',
    'Ν': 'N',
    'Ο': 'O',
    'Ρ': 'P',
    'Τ': 'T',
    'Υ': 'Y',
    'Χ': 'X',
    'ο': 'o',
    'υ': 'u',

    # Explicit unwanted markers
    '密': '',
    '掩': '',
}

CHAR_REPLACEMENTS = {
    '\u2018': "'",    # Left single quote
    '\u2019': "'",    # Right single quote
    '\u201C': '"',    # Left double quote
    '\u201D': '"',    # Right double quote
    '\u2013': '-',    # En dash
    '\u2014': '-',    # Em dash
    '\u2026': '...',  # Ellipsis
    '\u00A0': ' ',    # Non-breaking space
    '\u202F': ' ',    # Narrow no-break space
    '\u2007': ' ',    # Figure space
}


# ============================================================
# Helpers
# ============================================================

def unicode_info(char):
    codepoint = 'U+{:04X}'.format(ord(char))
    name = unicodedata.name(char, 'UNKNOWN CHARACTER')

    return '{} {}'.format(codepoint, name)


def display_char(char):
    if char == ' ':
        return '<SPACE>'

    if char == '\t':
        return '<TAB>'

    if char == '\n':
        return '<NEWLINE>'

    if not char:
        return '<REMOVED>'

    return repr(char)


# ============================================================
# DeWatermark Sanitizer
# ============================================================

def dewatermark(text):
    output = []

    removed = Counter()
    replaced = Counter()

    for char in text:

        # ----------------------------------------------------
        # Invisible characters
        # ----------------------------------------------------

        if char in INVISIBLE_CHARS:
            removed[char] += 1
            continue

        # ----------------------------------------------------
        # Homoglyphs / explicit markers
        # ----------------------------------------------------

        if char in HOMOGLYPH_MAP:
            replacement = HOMOGLYPH_MAP[char]

            if replacement == '':
                removed[char] += 1
            else:
                replaced[(char, replacement, 'homoglyph')] += 1

            output.append(replacement)
            continue

        # ----------------------------------------------------
        # Typography
        # ----------------------------------------------------

        if char in CHAR_REPLACEMENTS:
            replacement = CHAR_REPLACEMENTS[char]

            replaced[(char, replacement, 'typography')] += 1
            output.append(replacement)
            continue

        output.append(char)

    cleaned = ''.join(output)

    return cleaned, removed, replaced


# ============================================================
# Logging
# ============================================================

def log_results(original, cleaned, removed, replaced):
    print('')
    print('=' * 70)
    print('DeWatermark')
    print('=' * 70)

    if original == cleaned:
        print(
            'CLEAN - {} chars - no watermarks detected'.format(
                len(original)
            )
        )

        print('=' * 70)
        print('')
        return

    print(
        'CLEANED - {} -> {} chars'.format(
            len(original),
            len(cleaned)
        )
    )

    total_removed = sum(removed.values())
    total_replaced = sum(replaced.values())

    print('')
    print('Summary:')
    print('  Removed:  {}'.format(total_removed))
    print('  Replaced: {}'.format(total_replaced))

    # --------------------------------------------------------
    # Removed
    # --------------------------------------------------------

    if removed:
        print('')
        print('REMOVED:')

        for char, count in removed.items():
            print(
                '  {}x  {}  {}'.format(
                    count,
                    unicode_info(char),
                    display_char(char)
                )
            )

    # --------------------------------------------------------
    # Replaced
    # --------------------------------------------------------

    if replaced:
        print('')
        print('REPLACED:')

        for (char, replacement, category), count in replaced.items():
            print(
                '  {}x  {}  {} -> {}  [{}]'.format(
                    count,
                    unicode_info(char),
                    display_char(char),
                    display_char(replacement),
                    category.upper()
                )
            )

    print('')
    print('=' * 70)
    print('')


# ============================================================
# Sublime Commands
# ============================================================

class DewatermarkPasteCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        original = sublime.get_clipboard()

        if not original:
            print('DeWatermark: Clipboard is empty.')
            sublime.status_message('DeWatermark: Clipboard is empty.')
            return

        cleaned, removed, replaced = dewatermark(original)

        log_results(
            original,
            cleaned,
            removed,
            replaced
        )

        selections = list(self.view.sel())

        for region in reversed(selections):
            self.view.replace(edit, region, cleaned)

        total_removed = sum(removed.values())
        total_replaced = sum(replaced.values())

        if total_removed or total_replaced:
            sublime.status_message(
                'DeWatermark: Removed {} and replaced {} character(s).'.format(
                    total_removed,
                    total_replaced
                )
            )
        else:
            sublime.status_message(
                'DeWatermark: Clean - no watermarks detected.'
            )
