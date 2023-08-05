from os import listdir
from os.path import dirname, realpath
from re import compile as re_compile
from re import findall, IGNORECASE, MULTILINE, UNICODE
from re import finditer
import pickle
flags = MULTILINE|UNICODE


directory_of_this_file = dirname(realpath(__file__))

# load patterns
directory_of_patterns = directory_of_this_file + "/prep/patterns"
language_pattern = {}
for filename in listdir(directory_of_patterns):
    language = filename.split(".")[0]
    with open(directory_of_patterns + "/" + language + ".txt") as f:
        pattern_as_string = (f.read().decode("utf-8").strip())
        pattern = re_compile(pattern_as_string, flags=flags)
        language_pattern[language] = pattern

def flatten(lst):
    result = []
    for element in lst:
        if hasattr(element, '__iter__'):
            result.extend(flatten(element))
        else:
            result.append(element)
    return result


def extract_statements(text, language=None):

    if isinstance(text, str):
        text = text.decode("utf-8")

    statements = []
    if language:
        pass
    else:

        for pattern in language_pattern.values():
            for matchobject in finditer(pattern, text):
                dicts = {}
                for key, value in matchobject.groupdict().iteritems():
                    if value:
                        k1, k2 = key.split("_")
                        if k2 in dicts:
                            dicts[k2][k1] = value
                        else:
                            dicts[k2] = {k1: value}
                d = [v for k,v in dicts.iteritems() if len(v) >= 3]
                if d:
                    statements.append(d[0])

    return statements

def extract_statement(text):
    return extract_statements(text)[0]

def get_keywords():
    directory_of_keywords = directory_of_this_file + "/prep/keywords"
    language_keywords = {}
    for filename in listdir(directory_of_keywords):
        language = filename.split(".")[0]
        with open(directory_of_keywords + "/" + language + ".txt") as f:
            language_keywords[language] = f.read().decode("utf-8").strip().splitlines()
    return language_keywords
eo=extract_statements
