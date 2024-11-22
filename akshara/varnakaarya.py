"""Handles all operations on varnas"""

import sys

from akshara.varna import Varnamaalaa

vn = Varnamaalaa()


def check_vinyaasa(vinyaasa: list) -> None:
    """Checks is a vinyaasaa contains illegal characters

    Args:
        vinyaasa (list): Vinyaasa to be analysed
    """

    for symbol in vinyaasa:
        assert (
            symbol
            in vn.all_svaras
            + vn.all_vyanjanas
            + vn.avasaana
            + vn.sankhyaa
            + vn.ayogavaaha
            + ["ऽ", "\n", "(", ")", "{", "}", "[", "]"]
        ), f"Illegal varna {symbol} found in vinyaasaa {vinyaasa}"


def maarjaka(sentence: str) -> str:
    """Cleans up a string

    Args:
        sentence (str): String to be cleaned

    Returns:
        str: Clean string
    """

    sentence = sentence.rstrip("\n")

    return sentence


def count_svaras(vinyaasa: list) -> int:
    """Counts the number of svaras

    Args:
        vinyaasa (list): Vinyaasa of a string

    Returns:
        int: Number of svaras
    """

    return sum(1 for x in get_vinyaasa(vinyaasa) if x in vn.svara)


def count_vyanjanas(vinyaasa: list) -> int:
    """Counts the number of vyanjanas

    Args:
        vinyaasa (list | str): Vinyaasa of a string

    Returns:
        int: Number of vyanjanas
    """

    return sum(1 for x in get_vinyaasa(vinyaasa) if x in vn.vyanjana)


def count_ayogavaahas(vinyaasa: list) -> int:
    """Counts the number of ayogavaahas

    Args:
        vinyaasa (list | str): Vinyaasa of a string

    Returns:
        int: Number of ayogavaahas
    """

    return sum(1 for x in get_vinyaasa(vinyaasa) if x in vn.ayogavaaha)


def count_varnas(vinyaasa: list) -> int:
    """Counts the number of varnas

    Args:
        vinyaasa (list | str): Vinyaasa of a string

    Returns:
        int: Number of varnas
    """

    return (
        count_svaras(vinyaasa) + count_vyanjanas(vinyaasa) + count_ayogavaahas(vinyaasa)
    )


def count_vaakyas(vinyaasa: list) -> int:
    """Counts the number of vaakyas

    Args:
        vinyaasa (list): Vinyaasa of a string

    Returns:
        int: Number of vaakyas
    """

    return sum(1 for x in vinyaasa if x in ["।", "॥"])


def break_paada(vinyaasa: list) -> list:
    """Breaks a line into two equal paadas

    Args:
        vinyaasa (list): Vinyaasa of the string to be broken

    Returns:
        list: List containing two resultant vinyaasas
    """

    i = 0

    while count_svaras(vinyaasa[0:i]) < count_svaras(vinyaasa) / 2.0:
        i += 1

    if vinyaasa[i] in ["ः", "ं"] or vinyaasa[i] not in [" "]:
        i += 1

    return [vinyaasa[0:i], vinyaasa[i:]]


def add_akaara(shabda: str, index: int, vinyaasa: list) -> list:
    """Decides on the type of akaara (anunaasika or not) to be added in the vinyaasa and adds it

    Args:
        shabda (str): String in consideration
        index (int): Location in the string which is being considered
        vinyaasa (list): Current state of the vinyaasa

    Returns:
        list: Updated vinyaasa
    """

    if index + 1 < len(shabda):
        if (
            shabda[index + 1] in vn.vyanjana_with_akaara
            or shabda[index + 1] in vn.avasaana
            or shabda[index + 1] in ["ः", "ं", "३", "(", ")", "{", "}", "[", "]"]
        ):
            vinyaasa.append("अ")

        if shabda[index + 1] in ["ँ"]:
            vinyaasa.append("अँ")
    else:
        vinyaasa.append("अ")

    return vinyaasa


def combine_pluta(vinyaasa: list) -> list:
    """Combines all pluta markings with their svaras

    Args:
        vinyaasa (list): Vinyaasa in consideration

    Returns:
        list: Modified vinyaasa
    """

    while "३" in vinyaasa:
        index = vinyaasa.index("३")
        if vinyaasa[index - 1] in vn.svara + vn.anunaasika_svara:
            vinyaasa[index - 1] += "३"
            del vinyaasa[index]
        else:
            vinyaasa[index] = "a"

    vinyaasa = ["३" if x == "a" else x for x in vinyaasa]

    return vinyaasa


def split_pluta(vinyaasa: list) -> list:
    """Splits all pluta markings

    Args:
        vinyaasa (list): Vinyaasa in consideration

    Returns:
        list: Modified vinyaasa
    """

    index = 0

    while index < len(vinyaasa):
        if "३" not in vinyaasa[index]:
            index += 1
        else:
            vinyaasa[index] = vinyaasa[index][:-1]
            vinyaasa.insert(index + 1, "३")
            index += 2

    return vinyaasa


def get_vinyaasa(shabda: str) -> list:
    """Returns the vinyaasa (spelling) of a string

    Args:
        shabda (str): String to be spelled

    Returns:
        str: Spelling of the string
    """

    shabda = maarjaka(shabda)
    vinyaasa = []

    for index, element in enumerate(shabda):
        if element in vn.svara:
            vinyaasa.append(element)
        elif element in vn.vyanjana_with_akaara:
            if (
                len(shabda) > index + 2
                and shabda[index + 1] == "्"
                and shabda[index + 2] == "ँ"
            ):
                vinyaasa.append(element + "्" + "ँ")
            else:
                vinyaasa.append(element + "्")
            vinyaasa = add_akaara(shabda, index, vinyaasa)
        elif element in vn.maatraa:
            if index + 1 < len(shabda):
                if shabda[index + 1] in ["ँ"]:
                    vinyaasa.append(vn.maatraa_to_svara[element] + "ँ")
                else:
                    vinyaasa.append(vn.maatraa_to_svara[element])
            else:
                vinyaasa.append(vn.maatraa_to_svara[element])
        elif element in ["्", "ँ"]:
            pass
        else:
            vinyaasa.append(element)

    check_vinyaasa(vinyaasa)

    vinyaasa = combine_pluta(vinyaasa)

    return vinyaasa


def get_shabda(vinyaasa: list) -> str:
    """Reconstructs a string from a vinyaasa (spelling)

    Args:
        vinyaasa (list): Spelling of the string

    Returns:
        str: Reconstructed string
    """

    vinyaasa = split_pluta(vinyaasa)

    shabda = ""

    for index, varna in enumerate(vinyaasa):
        if index == 0 and varna in vn.svara:
            symbol = varna
        elif varna in vn.svara and (
            vinyaasa[index - 1] in vn.svara
            or vinyaasa[index - 1] in [" ", "।", "॥", "(", ")", "{", "}", "[", "]"]
        ):
            symbol = varna
        elif varna in vn.vyanjana and index + 1 < len(vinyaasa):
            if (
                vinyaasa[index + 1] in vn.svara
                or vinyaasa[index + 1] in vn.anunaasika_svara
            ):
                symbol = varna[0]
            else:
                symbol = varna
        elif varna == "अ":
            symbol = ""
        elif varna == "अँ":
            symbol = "ँ"
        elif varna in vn.svara and vinyaasa[index - 1] in vn.vyanjana:
            symbol = vn.svara_to_maatraa[varna]
        elif varna in vn.anunaasika_svara:
            symbol = vn.svara_to_maatraa[varna[0]] + "ँ"
        else:
            symbol = varna

        shabda = shabda + symbol

    return shabda


def get_sankhyaa(roman: str) -> str:
    """Converts romal numerals to devanaagari

    Args:
        s (str): Roman number in string form

    Returns:
        str: Devanaagari number in string form
    """

    devanaagari = ""
    roman = str(roman)

    for digit in roman:
        if digit == ".":
            devanaagari += digit
        elif int(digit) < 0 or int(digit) > 9:
            print(f"{digit} is Not a digit")
            sys.exit()
        else:
            devanaagari += vn.sankhyaa[int(digit)]

    return devanaagari


def get_akshara(vinyaasa: list) -> list:
    """Returns the akshara (syllable) of a string

    Args:
        vinyaasa (list): Vinyaasa of the string

    Returns:
        list: Syllables of the string
    """

    index_svara = [
        i for i, x in enumerate(vinyaasa) if x in vn.svara or x in vn.anunaasika_svara
    ]

    akshara = []
    start = 0
    for i in index_svara:
        akshara.append(get_shabda(vinyaasa[start : i + 1]))
        start = i + 1

    print(index_svara)

    if index_svara and index_svara[-1] != len(vinyaasa) - 1:

        if len(akshara) == 1:
            akshara = [get_shabda(vinyaasa)]

        else:
            akshara[-1] = get_shabda(vinyaasa[index_svara[-2] + 1 :])

    return akshara
