"""Contructs a list of varnas with all properties"""

import yaml

with open("varna.yml", "r", encoding="utf-8") as file:
    dd = yaml.safe_load(file)

with open("moola.csv", "w", encoding="utf-8") as file:
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

with open("vistrita.csv", "w", encoding="utf-8") as file:
    for v in dd.keys():
        dd[v]["नासिकभेदः"] = "निरनुनासिकः"

        if dd[v]["भेदः"] == "स्वरः":
            for naasika in ["", "ँ"]:
                if naasika == "ँ":
                    dd[v]["नासिकभेदः"] = "अनुनासिकः"
                    dd[v]["उच्चारणस्थानम्"] = dd[v]["उच्चारणस्थानम्"] + "+" + "नासिका"

                for baahyaprayatna in ["उदात्तः", "अनुदात्तः", "स्वरितः"]:
                    dd[v]["बाह्यप्रयत्नः"] = baahyaprayatna

                    if baahyaprayatna == "अनुदात्तः":
                        CHINHA = "॒"
                    elif baahyaprayatna == "स्वरितः":
                        CHINHA = "॑"
                    else:
                        CHINHA = ""

                    line = (
                        v + naasika + CHINHA
                        if len(v) == 1
                        else v[0] + naasika + CHINHA + v[1]
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
                    dd[v]["उच्चारणस्थानम्"] = dd[v]["उच्चारणस्थानम्"] + "+" + "नासिका"

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

with open("vistrita.csv", "r", encoding="utf-8") as file:
    lines = file.readlines()


with open("laukika.csv", "w", encoding="utf-8") as file:
    for line in lines:
        if "॒" not in line and "॑" not in line and "यमः" not in line:
            file.write(line)

with open("latest.csv", "w", encoding="utf-8") as file:

    for line in lines:
        if "॒" not in line and "॑" not in line and "यमः" not in line:
            file.write(line.replace("संवृतः", "विवृतः"))
