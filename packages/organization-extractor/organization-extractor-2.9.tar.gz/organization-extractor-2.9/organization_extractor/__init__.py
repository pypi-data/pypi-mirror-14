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


def extract_organizations(text, language=None):

    if isinstance(text, str):
        text = text.decode("utf-8")

    organizations = set()
    if language:

        organizations.update(flatten(findall(language_pattern[language], text)))

    else:

        for pattern in language_pattern.values():
            organizations.update(flatten(findall(pattern, text)))

    organizations = [org for org in list(organizations) if org and org.count(" ") > 0]

    return organizations

def extract_organization(text):
    return extract_organizations(text)[0]

def get_keywords():
    directory_of_keywords = directory_of_this_file + "/prep/keywords"
    language_keywords = {}
    for filename in listdir(directory_of_keywords):
        language = filename.split(".")[0]
        with open(directory_of_keywords + "/" + language + ".txt") as f:
            language_keywords[language] = f.read().decode("utf-8").strip().splitlines()
    return language_keywords
eo=extract_organizations
