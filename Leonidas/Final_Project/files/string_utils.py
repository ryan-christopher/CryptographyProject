# crypto_project/string_utils.py

def color_string(text, print_red=False):
    """
    Färbt einen Text auf der Konsole ein.
    Grün für normal, rot für Fehler / Attack.
    """
    bold_red = "\033[1;31m"
    green = "\033[32m"
    reset_color = "\033[0m"
    text_color = bold_red if print_red else green
    return text_color + str(text) + reset_color


def join_strings(items, delimiter):
    """
    Verbindet eine Liste von Strings mit einem Delimiter.
    Extra einfach geschrieben, so wie man es als Student machen würde.
    """
    result = ""
    for index, part in enumerate(items):
        result += str(part)
        if index < len(items) - 1:
            result += delimiter
    return result


def lower_string(s):
    """
    Liefert eine kleingeschriebene Version eines Strings zurück.
    """
    return str(s).lower()
