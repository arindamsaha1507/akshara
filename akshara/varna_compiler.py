"""Contructs a list of varnas with all properties"""
import os
import yaml


def create_varna_table(
    input_file="varna.yml",
    moola="moola.csv",
    laukika="laukika.csv",
    vistrita="vistrita.csv",
    latest="latest.csv",
    directory="resources",
):
    """Creates varna tables

    Args:
        input (str, optional): Input filename for varnas (yaml). Defaults to "varna.yml".
        moola (str, optional): Output filename for moola. Defaults to "moola.csv".
        laukika (str, optional): Output filname for laukika. Defaults to "laukika.csv".
        vistrita (str, optional): Output filename for vistrita. Defaults to "vistrita.csv".
        latest (str, optional): Output filename for latest. Defaults to "latest.csv".
        directory (str, optional): Resource directory. Defaults to "resources".
    """

    path = f"{str(os.path.dirname(__file__))}/{directory}"
    print(os.path.dirname(__file__))
    input_fname = f"{path}/{input_file}"
    moola_fname = f"{path}/{moola}"
    laukika_fname = f"{path}/{laukika}"
    vistrita_fname = f"{path}/{vistrita}"
    latest_fname = f"{path}/{latest}"

    with open(input_fname, "r", encoding="utf-8") as file:
        dd = yaml.safe_load(file)

    with open(moola_fname, "w", encoding="utf-8") as file:
        for v in dd.keys():
            if "आभ्यन्तरप्रयत्नः" not in dd[v].keys():
                dd[v]["आभ्यन्तरप्रयत्नः"] = "-"

            if "बाह्यप्रयत्नः" not in dd[v].keys():
                dd[v]["बाह्यप्रयत्नः"] = "-"

            if "कालः" not in dd[v].keys():
                dd[v]["कालः"] = "-"

            if isinstance(dd[v]["उच्चारणस्थानम्"], list):
                dd[v]["उच्चारणस्थानम्"] = "+".join(dd[v]["उच्चारणस्थानम्"])

            if isinstance(dd[v]["बाह्यप्रयत्नः"], list):
                dd[v]["बाह्यप्रयत्नः"] = "+".join(dd[v]["बाह्यप्रयत्नः"])

            line = v
            line += f",{dd[v]['भेदः']},{dd[v]['उच्चारणस्थानम्']}"
            line += f",{dd[v]['आभ्यन्तरप्रयत्नः']},{dd[v]['बाह्यप्रयत्नः']}"
            line += f",{dd[v]['कालः']}"
            line += "\n"

            file.write(line)

    with open(vistrita_fname, "w", encoding="utf-8") as file:
        for v in dd.keys():
            dd[v]["नासिकभेदः"] = "निरनुनासिकः"

            if dd[v]["भेदः"] == "स्वरः":
                for naasika in ["", "ँ"]:
                    if naasika == "ँ":
                        dd[v]["नासिकभेदः"] = "अनुनासिकः"
                        dd[v]["उच्चारणस्थानम्"] = (
                            dd[v]["उच्चारणस्थानम्"] + "+" + "नासिका"
                        )

                    for baahyaprayatna in ["उदात्तः", "अनुदात्तः", "स्वरितः"]:
                        dd[v]["बाह्यप्रयत्नः"] = baahyaprayatna

                        if baahyaprayatna == "अनुदात्तः":
                            chinha = "॒"
                        elif baahyaprayatna == "स्वरितः":
                            chinha = "॑"
                        else:
                            chinha = ""

                        line = (
                            v + naasika + chinha
                            if len(v) == 1
                            else v[0] + naasika + chinha + v[1]
                        )
                        line += f",{dd[v]['भेदः']},{dd[v]['उच्चारणस्थानम्']}"
                        line += f",{dd[v]['आभ्यन्तरप्रयत्नः']},{dd[v]['बाह्यप्रयत्नः']}"
                        line += f",{dd[v]['कालः']},{dd[v]['नासिकभेदः']}"
                        line += "\n"

                        file.write(line)

            elif v in ["य्", "ल्", "व्"]:
                for naasika in ["", "ँ"]:
                    if naasika == "ँ":
                        dd[v]["नासिकभेदः"] = "अनुनासिकः"
                        dd[v]["उच्चारणस्थानम्"] = (
                            dd[v]["उच्चारणस्थानम्"] + "+" + "नासिका"
                        )

                    line = v + naasika
                    line += f",{dd[v]['भेदः']},{dd[v]['उच्चारणस्थानम्']}"
                    line += f",{dd[v]['आभ्यन्तरप्रयत्नः']},{dd[v]['बाह्यप्रयत्नः']}"
                    line += f",{dd[v]['कालः']},{dd[v]['नासिकभेदः']}"
                    line += "\n"

                    file.write(line)

            else:
                if "आभ्यन्तरप्रयत्नः" not in dd[v].keys():
                    dd[v]["आभ्यन्तरप्रयत्नः"] = "-"

                if "बाह्यप्रयत्नः" not in dd[v].keys():
                    dd[v]["बाह्यप्रयत्नः"] = "-"

                if "कालः" not in dd[v].keys():
                    dd[v]["कालः"] = "-"

                if "+" in dd[v]["उच्चारणस्थानम्"]:
                    if "नासिका" in dd[v]["उच्चारणस्थानम्"]:
                        dd[v]["नासिकभेदः"] = "अनुनासिकः"

                line = v
                line += f",{dd[v]['भेदः']},{dd[v]['उच्चारणस्थानम्']}"
                line += f",{dd[v]['आभ्यन्तरप्रयत्नः']},{dd[v]['बाह्यप्रयत्नः']}"
                line += f",{dd[v]['कालः']},{dd[v]['नासिकभेदः']}"
                line += "\n"

                file.write(line)

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
