"""Handles all operations on varnas"""

import sys

import akshara.varna as vn


def maarjaka(sentence: str) -> str:
    """Cleans up a string

    Args:
        sentence (str): String to be cleaned

    Returns:
        str: Clean string
    """

    sentence = sentence.rstrip("\n")

    return sentence


def count_svaras(vinyaasa: list | str) -> int:
    """Counts the number of svaras

    Args:
        vinyaasa (list | str): String or vinyaasa of a string

    Returns:
        int: Number of svaras
    """

    return sum(1 for x in get_vinyaasa(vinyaasa) if x in vn.svara)


def count_vyanjanas(vinyaasa: list | str) -> int:
    """Counts the number of vyanjanas

    Args:
        vinyaasa (list | str): String or vinyaasa of a string

    Returns:
        int: Number of vyanjanas
    """

    return sum(1 for x in get_vinyaasa(vinyaasa) if x in vn.vyanjana)


def count_vaakyas(vinyaasa: list | str) -> int:
    """Counts the number of vaakyas

    Args:
        vinyaasa (list | str): String or vinyaasa of a string

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
            or shabda[index + 1] in ["ः", "ं"]
        ):
            vinyaasa.append("अ")

        if shabda[index + 1] in ["ँ"]:
            vinyaasa.append("अँ")
    else:
        vinyaasa.append("अ")

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

    return vinyaasa


def get_shabda(vinyaasa: list) -> str:
    """Reconstructs a string from a vinyaasa (spelling)

    Args:
        vinyaasa (list): Spelling of the string

    Returns:
        str: Reconstructed string
    """

    shabda = ""

    for index, varna in enumerate(vinyaasa):
        if index == 0 and varna in vn.svara:
            symbol = varna
        elif varna in vn.svara and (
            vinyaasa[index - 1] in vn.svara or vinyaasa[index - 1] == " "
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
        elif varna in vn.svara:
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


def expand_pratyahaara(pratyaahaara: str) -> list:
    """Expands a pratyaahaara

    Args:
        pratyaahaara (str): Pratyaahaara to be expanded

    Returns:
        list: List to varnas in expansion of the pratyaahaara
    """

    assert len(pratyaahaara) == 3
    assert pratyaahaara[2] == "्"

    start = pratyaahaara[0]
    stop = pratyaahaara[1] + pratyaahaara[2]

    i = vn.maaheshwar_suutra.index(start)
    j = vn.maaheshwar_suutra.index(stop)

    section = vn.maaheshwar_suutra[i:j]

    it_letter = [x for x in section if x in vn.vyanjana]
    for letter in it_letter:
        section.remove(letter)

    section = [x + "्" if x in vn.vyanjana_with_akaara else x for x in section]

    if "अ" in section:
        section.append("आ")
    if "इ" in section:
        section.append("ई")
    if "उ" in section:
        section.append("ऊ")

    return list(set(section))
