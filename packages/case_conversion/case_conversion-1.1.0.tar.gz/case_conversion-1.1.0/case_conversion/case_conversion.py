import sys

PYTHON = sys.version_info[0]

if 3 == PYTHON:
    # Python 3 and ST3
    from . import case_parse
else:
    # Python 2 and ST2
    import case_parse


def camelcase(text, detectAcronyms=False, acronyms=[]):
    words, case, sep = case_parse.parseVariable(text, detectAcronyms, acronyms)
    if words:
        words[0] = words[0].lower()
    return ''.join(words)


def pascalcase(text, detectAcronyms=False, acronyms=[]):
    words, case, sep = case_parse.parseVariable(text, detectAcronyms, acronyms)
    return ''.join(words)


def snakecase(text, detectAcronyms=False, acronyms=[]):
    words, case, sep = case_parse.parseVariable(text, detectAcronyms, acronyms)
    return '_'.join([w.lower() for w in words])


def dashcase(text, detectAcronyms=False, acronyms=[]):
    words, case, sep = case_parse.parseVariable(text, detectAcronyms, acronyms)
    return '-'.join([w.lower() for w in words])


def kebabcase(text, detectAcronyms=False, acronyms=[]):
    return dashcase(text, detectAcronyms, acronyms)


def spinalcase(text, detectAcronyms=False, acronyms=[]):
    return dashcase(text, detectAcronyms, acronyms)


def constcase(text, detectAcronyms=False, acronyms=[]):
    words, case, sep = case_parse.parseVariable(text, detectAcronyms, acronyms)
    return '_'.join([w.upper() for w in words])


def dotcase(text, detectAcronyms=False, acronyms=[]):
    words, case, sep = case_parse.parseVariable(text, detectAcronyms, acronyms)
    return '.'.join([w.lower() for w in words])


def separate_words(text, detectAcronyms=False, acronyms=[]):
    words, case, sep = case_parse.parseVariable(text, detectAcronyms, acronyms, preserveCase=True)
    return ' '.join(words)


def slashcase(text, detectAcronyms=False, acronyms=[]):
    words, case, sep = case_parse.parseVariable(text, detectAcronyms, acronyms, preserveCase=True)
    return '/'.join(words)


def backslashcase(text, detectAcronyms=False, acronyms=[]):
    words, case, sep = case_parse.parseVariable(text, detectAcronyms, acronyms, preserveCase=True)
    return '\\'.join(words)
