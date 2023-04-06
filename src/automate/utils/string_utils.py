import re


def slugify(string: str, sub: str = "-") -> str:
    """
    Slugifies a string.

    :param string: string to slugify
    :return: slugified string
    """
    # replace all non-word characters (everything except numbers and letters) with a space
    string = re.sub(r"[^\w\s]", " ", string)
    # replace all runs of whitespace with a single dash
    string = re.sub(r"\s+", sub, string)
    # remove leading and trailing whitespace
    string = string.strip()
    # make lowercase
    string = string.lower()
    return string
