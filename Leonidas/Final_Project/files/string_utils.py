# crypto_project/string_utils.py

def color_string(text, print_red=False):
    """
    Colors a text on the console.
    Green for normal, red for error / attack.
    """
    bold_red = "\033[1;31m"
    green = "\033[32m"
    reset_color = "\033[0m"
    text_color = bold_red if print_red else green
    return text_color + str(text) + reset_color


def join_strings(items, delimiter):
    """
    Connects a list of strings with a delimiter.
    """
    result = ""
    for index, part in enumerate(items):
        result += str(part)
        if index < len(items) - 1:
            result += delimiter
    return result


def lower_string(s):
    """
    Returns a lowercase version of a string.
    """
    return str(s).lower()
