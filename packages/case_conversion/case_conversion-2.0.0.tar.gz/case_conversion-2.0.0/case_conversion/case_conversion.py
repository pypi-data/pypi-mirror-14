import sys

PYTHON = sys.version_info[0]

if 3 == PYTHON:
    # Python 3 and ST3
    from . import case_parse
else:
    # Python 2 and ST2
    import case_parse


def camelcase(text, detect_acronyms=False, acronyms=[]):
    words, case, sep = case_parse.parse_case(text, detect_acronyms, acronyms)
    if words:
        words[0] = words[0].lower()
    return ''.join(words)


def pascalcase(text, detect_acronyms=False, acronyms=[]):
    words, case, sep = case_parse.parse_case(text, detect_acronyms, acronyms)
    return ''.join(words)


def snakecase(text, detect_acronyms=False, acronyms=[]):
    words, case, sep = case_parse.parse_case(text, detect_acronyms, acronyms)
    return '_'.join([w.lower() for w in words])


def dashcase(text, detect_acronyms=False, acronyms=[]):
    words, case, sep = case_parse.parse_case(text, detect_acronyms, acronyms)
    return '-'.join([w.lower() for w in words])


def kebabcase(text, detect_acronyms=False, acronyms=[]):
    return dashcase(text, detect_acronyms, acronyms)


def spinalcase(text, detect_acronyms=False, acronyms=[]):
    return dashcase(text, detect_acronyms, acronyms)


def constcase(text, detect_acronyms=False, acronyms=[]):
    words, case, sep = case_parse.parse_case(text, detect_acronyms, acronyms)
    return '_'.join([w.upper() for w in words])


def dotcase(text, detect_acronyms=False, acronyms=[]):
    words, case, sep = case_parse.parse_case(text, detect_acronyms, acronyms)
    return '.'.join([w.lower() for w in words])


def separate_words(text, detect_acronyms=False, acronyms=[]):
    words, case, sep = case_parse.parse_case(
        text, detect_acronyms, acronyms, preserve_case=True)
    return ' '.join(words)


def slashcase(text, detect_acronyms=False, acronyms=[]):
    words, case, sep = case_parse.parse_case(
        text, detect_acronyms, acronyms, preserve_case=True)
    return '/'.join(words)


def backslashcase(text, detect_acronyms=False, acronyms=[]):
    words, case, sep = case_parse.parse_case(
        text, detect_acronyms, acronyms, preserve_case=True)
    return '\\'.join(words)
