import unicodedata


def normalize_str(input_str: str):
    """
    Normaliza e remove acentos de uma string.
    :param input_str: String que será normalizada.
    :return: String normalizada.
    """
    nfd_form = unicodedata.normalize('NFD', input_str)
    only_ascii = nfd_form.encode('ASCII', 'ignore')
    return only_ascii.decode()
