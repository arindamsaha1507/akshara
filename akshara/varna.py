"""Defines basic alphabet for sanskrit"""

import os
import yaml


def read_table(filename="latest.csv", directory="resources") -> list:
    """Read varna table

    Args:
        filename (str, optional): Filename of resource table. Defaults to 'latest.csv'.
        directory (str, optional): Resource directory. Defaults to 'resources'.

    Returns:
        list: List of lines read
    """

    path = f"{str(os.path.dirname(__file__))}/{directory}/{filename}"

    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    return list(lines)


def read_symbols(filename="vividha.yml", directory="resources") -> dict:
    """Read symbols file

    Args:
        filename (str, optional): Symbols filename. Defaults to 'vividha.yml'.
        directory (str, optional): Resource directory. Defaults to 'resources'.

    Returns:
        dict: Dict of yaml file read
    """

    path = f"{str(os.path.dirname(__file__))}/{directory}/{filename}"
    with open(path, "r", encoding="utf-8") as symbol_file:
        symbols = yaml.safe_load(symbol_file)

        return symbols


def get_svara(raw_lines: list) -> list:
    """Returns list of svaras

    Args:
        raw_lines (list): List of lines read from the resources

    Returns:
        list: List of svaras
    """

    return list(x.split(",")[0] for x in raw_lines if x.split(",")[1] == "स्वरः")


def get_vyanjana(raw_lines: list) -> list:
    """Returns list of vyanjanas

    Args:
        raw_lines (list): List of lines read from the resources

    Returns:
        list: List of vyanjanas
    """

    return list(x.split(",")[0] for x in raw_lines if x.split(",")[1] == "व्यञ्जनम्")


resource_lines = read_table()
all_svara = get_svara(resource_lines)
vyanjana = get_vyanjana(resource_lines)
vyanjana_with_akaara = list(x[0] for x in vyanjana)
avasaana = [" ", "।", "॥", "-"]
anunaasika_svara = list(x for x in all_svara if "ँ" in x)
niranunaasika_svara = list(x for x in all_svara if "ँ" not in x)
svara = list(x for x in niranunaasika_svara if "३" not in x)

other_symbols = read_symbols()

maatraa = other_symbols["maatraa"]

maatraa_to_svara = dict(zip(maatraa, svara[1:]))
svara_to_maatraa = dict(zip(svara[1:], maatraa))

sankhyaa = other_symbols["sankhyaa"]

maaheshwara_sutra = other_symbols["maaheshwara_sutra"]
