"""Contructs a list of varnas with all properties"""
import os

import yaml


def write_csv(parts: list, filename: str):
    """Writes properties of a single varna to a csv file

    Args:
        parts (list): List of components to be written
        filename (str): Filename of the output file
    """

    with open(filename, "a", encoding="utf-8") as file:
        for index, part in enumerate(parts):
            file.write(part)
            if index == len(parts) - 1:
                file.write("\n")
            else:
                file.write(",")


def create_moola(data_dict: dict, moola_fname: str):
    """Creates moola varna table

    Args:
        data_dict (dict): Data dictionary containing all information
        moola_fname (str): Output filename
    """

    os.remove(moola_fname)

    for data_key in data_dict.keys():
        if "आभ्यन्तरप्रयत्नः" not in data_dict[data_key].keys():
            data_dict[data_key]["आभ्यन्तरप्रयत्नः"] = "-"

        if "बाह्यप्रयत्नः" not in data_dict[data_key].keys():
            data_dict[data_key]["बाह्यप्रयत्नः"] = "-"

        if "कालः" not in data_dict[data_key].keys():
            data_dict[data_key]["कालः"] = "-"

        if isinstance(data_dict[data_key]["उच्चारणस्थानम्"], list):
            data_dict[data_key]["उच्चारणस्थानम्"] = "+".join(
                data_dict[data_key]["उच्चारणस्थानम्"]
            )

        if isinstance(data_dict[data_key]["बाह्यप्रयत्नः"], list):
            data_dict[data_key]["बाह्यप्रयत्नः"] = "+".join(
                data_dict[data_key]["बाह्यप्रयत्नः"]
            )

        parts = [
            data_key,
            data_dict[data_key]["भेदः"],
            data_dict[data_key]["उच्चारणस्थानम्"],
            data_dict[data_key]["आभ्यन्तरप्रयत्नः"],
            data_dict[data_key]["बाह्यप्रयत्नः"],
            data_dict[data_key]["कालः"],
        ]

        write_csv(parts, moola_fname)


def handle_anunaasika(data: dict, naasika: str) -> dict:
    """Modifies data according to anunaasika

    Args:
        data (dict): Original data

    Returns:
        dict: Modified data
    """

    if naasika == "ँ":
        data["नासिकभेदः"] = "अनुनासिकः"
        data["उच्चारणस्थानम्"] = data["उच्चारणस्थानम्"] + "+" + "नासिका"

    return data


def get_svara_chinha(svara_bheda: str) -> str:
    """Returns svarachinha according to svarabheda

    Args:
        svara_bheda (str): Svarabheda

    Returns:
        str: Svarachinha
    """

    if svara_bheda == "अनुदात्तः":
        chinha = "॒"
    elif svara_bheda == "स्वरितः":
        chinha = "॑"
    else:
        chinha = ""

    return chinha


def create_vistrita(data_dict, vistrita_fname):
    """Creates vistrita varna table

    Args:
        data_dict (dict): Data dictionary containing all information
        moola_fname (str): Output filename
    """

    os.remove(vistrita_fname)

    for data_key in data_dict.keys():
        data_dict[data_key]["नासिकभेदः"] = "निरनुनासिकः"

        if data_dict[data_key]["भेदः"] == "स्वरः":
            for naasika in ["", "ँ"]:
                data_dict[data_key] = handle_anunaasika(data_dict[data_key], naasika)

                for baahyaprayatna in ["उदात्तः", "अनुदात्तः", "स्वरितः"]:
                    data_dict[data_key]["बाह्यप्रयत्नः"] = baahyaprayatna

                    chinha = get_svara_chinha(baahyaprayatna)

                    temp = (
                        data_key + naasika + chinha
                        if len(data_key) == 1
                        else data_key[0] + naasika + chinha + data_key[1]
                    )

                    parts = [
                        temp,
                        data_dict[data_key]["भेदः"],
                        data_dict[data_key]["उच्चारणस्थानम्"],
                        data_dict[data_key]["आभ्यन्तरप्रयत्नः"],
                        data_dict[data_key]["बाह्यप्रयत्नः"],
                        data_dict[data_key]["कालः"],
                        data_dict[data_key]["नासिकभेदः"],
                    ]

                    write_csv(parts, vistrita_fname)

        elif data_key in ["य्", "ल्", "व्"]:
            for naasika in ["", "ँ"]:
                data_dict[data_key] = handle_anunaasika(data_dict[data_key], naasika)

                temp = data_key + naasika

                parts = [
                    temp,
                    data_dict[data_key]["भेदः"],
                    data_dict[data_key]["उच्चारणस्थानम्"],
                    data_dict[data_key]["आभ्यन्तरप्रयत्नः"],
                    data_dict[data_key]["बाह्यप्रयत्नः"],
                    data_dict[data_key]["कालः"],
                    data_dict[data_key]["नासिकभेदः"],
                ]

                write_csv(parts, vistrita_fname)

        else:
            if "आभ्यन्तरप्रयत्नः" not in data_dict[data_key].keys():
                data_dict[data_key]["आभ्यन्तरप्रयत्नः"] = "-"

            if "बाह्यप्रयत्नः" not in data_dict[data_key].keys():
                data_dict[data_key]["बाह्यप्रयत्नः"] = "-"

            if "कालः" not in data_dict[data_key].keys():
                data_dict[data_key]["कालः"] = "-"

            if "+" in data_dict[data_key]["उच्चारणस्थानम्"]:
                if "नासिका" in data_dict[data_key]["उच्चारणस्थानम्"]:
                    data_dict[data_key]["नासिकभेदः"] = "अनुनासिकः"

            parts = [
                data_key,
                data_dict[data_key]["भेदः"],
                data_dict[data_key]["उच्चारणस्थानम्"],
                data_dict[data_key]["आभ्यन्तरप्रयत्नः"],
                data_dict[data_key]["बाह्यप्रयत्नः"],
                data_dict[data_key]["कालः"],
                data_dict[data_key]["नासिकभेदः"],
            ]

            write_csv(parts, vistrita_fname)


def create_varna_table(
    input_file="resources/varna.yml",
    moola="resources/moola.csv",
    laukika="resources/laukika.csv",
    vistrita="resources/vistrita.csv",
    latest="resources/latest.csv",
):
    """Creates varna tables

    Args:
        input (str, optional): Input file for varnas (yaml). Defaults to "resources/varna.yml".
        moola (str, optional): Output file for moola. Defaults to "resources/moola.csv".
        laukika (str, optional): Output file for laukika. Defaults to "resources/laukika.csv".
        vistrita (str, optional): Output file for vistrita. Defaults to "resources/vistrita.csv".
        latest (str, optional): Output file for latest. Defaults to "resources/latest.csv".
    """

    path = f"{str(os.path.dirname(__file__))}"
    input_fname = f"{path}/{input_file}"
    moola_fname = f"{path}/{moola}"
    laukika_fname = f"{path}/{laukika}"
    vistrita_fname = f"{path}/{vistrita}"
    latest_fname = f"{path}/{latest}"

    with open(input_fname, "r", encoding="utf-8") as file:
        data_dict = yaml.safe_load(file)

    create_moola(data_dict, moola_fname)
    create_vistrita(data_dict, vistrita_fname)

    with open(vistrita_fname, "r", encoding="utf-8") as file:
        lines = file.readlines()

    with open(laukika_fname, "w", encoding="utf-8") as file:
        for line in lines:
            if "॒" not in line and "॑" not in line and "यमः" not in line:
                file.write(line)

    with open(latest_fname, "w", encoding="utf-8") as file:
        for line in lines:
            if "॒" not in line and "॑" not in line and "यमः" not in line:
                file.write(line.replace("संवृतः", "विवृतः"))


if __name__ == "__main__":
    create_varna_table()
