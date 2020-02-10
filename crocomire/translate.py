from yaml import safe_load


def translate(word: str, filename: str):
    """
    Return a translated name from the given YAML file.

    :return: str
    """
    synData = safe_load(open(filename))

    synList = list(synData.keys())
    if word in synList:
        return word

    for i in synList:
        if word in synData[i]:
            return i

    return ""
