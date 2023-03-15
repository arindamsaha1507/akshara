"""Defines basic alphabet for sanskrit"""

import os
import yaml


def read_table(filename="latest.csv", directory="resources"):
    """Read varna table

    Args:
        filename (str, optional): Directory of resource table. Defaults to 'latest.csv'.
        directory (str, optional): Resource table filename. Defaults to 'resources'.

    Returns:
        list: List of lines read
    """

    path = f"{str(os.path.dirname(__file__))}/{directory}/{filename}"

    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    return list(lines)


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

directory = "resources"
filename = "vividha.yml"
path = f"{str(os.path.dirname(__file__))}/{directory}/{filename}"
with open(path, "r", encoding="utf-8") as symbol_file:
    symbols = yaml.safe_load(symbol_file)

maatraa = symbols["maatraa"]

maatraa_to_svara = dict(zip(maatraa, svara[1:]))
svara_to_maatraa = dict(zip(svara[1:], maatraa))

sankhyaa = symbols["sankhyaa"]

maaheshwara_sutra = symbols["maaheshwara_sutra"]
