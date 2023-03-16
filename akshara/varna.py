"""Defines basic alphabet for sanskrit"""

import os

import yaml


class Varna:
    """Class describing a single varna"""

    def __init__(self, line: str) -> None:
        parts = line.split(",")
        self.roopa = parts[0]
        self.bheda = parts[1]
        self.sthaana = parts[2]
        self.aabhyantara = parts[3]
        self.baahya = parts[4]
        self.kaala = parts[5]
        self.anunaasika = parts[6] == "अनुनासिकः"

    def get_roopa(self) -> str:
        """Returns the letter (roopa)"""
        return self.roopa

    def describe(self) -> None:
        """Prints description of the varna"""
        print(f"{self.roopa}, {self.sthaana}, {self.aabhyantara}")

    def is_svara(self) -> bool:
        """Checks if varna is svara"""
        return self.bheda == "स्वरः"

    def is_vyanjana(self) -> bool:
        """Checks if varna is vyanjana"""
        return self.bheda == "व्यञ्जनम्"

    def is_anunaasika(self) -> bool:
        """Checks if varna is anunaasika"""
        return self.anunaasika


class Varnamaalaa:
    """Class describing the varnamaalaa"""

    def __init__(self, varna_file_path: str, vividha_file_path: str) -> None:
        with open(varna_file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        with open(vividha_file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        self.varnamaalaa = list(Varna(line) for line in lines)
        self.maaheshwara_sutra = data["maaheshwara_sutra"]
        self.maatraa = data["maatraa"]
        self.varnas = [x.get_roopa() for x in self.varnamaalaa]

    def get_savarna(self, varna: str) -> list:
        """Returns savarnas of a varna

        Args:
            varna (str): Input varna

        Returns:
            list: List of savarnas
        """

        ref = list(x for x in self.varnamaalaa if x.get_roopa() == varna)

        assert len(ref) == 1

        ref = ref[0]

        test1 = list(
            x.get_roopa()
            for x in self.varnamaalaa
            if [x.bheda, x.sthaana, x.aabhyantara]
            == [ref.bheda, ref.sthaana, ref.aabhyantara]
        )

        test2 = list(
            x.get_roopa()
            for x in self.varnamaalaa
            if [x.bheda, x.sthaana, x.aabhyantara]
            == [ref.bheda, ref.sthaana + "+नासिका", ref.aabhyantara]
        )

        if "ऋ" in test1:
            test1.extend(["ऌ", "ऌ३"])

        if "ऋँ" in test2:
            test2.extend(["ऌँ", "ऌँ३"])

        return test1 + test2

    def get_varna(self, string: str) -> Varna:
        """Converts a varna character to Varna object

        Args:
            string (str): Varna character

        Returns:
            Varna: Varna object
        """
        varna = list(x for x in self.varnamaalaa if x.get_roopa() == string)

        assert len(varna) == 1

        return varna[0]

    def expand(self, code: str) -> list:
        """Pratyaahaaragrahana or savarnagrahana

        Args:
            code (str): Pratyaahaara or savarnagraahi

        Returns:
            list: List of varna
        """

        assert len(code) <= 3

        if (
            len(code) == 2
            and code[1] == self.maatraa[3]
            and self.get_varna(code[0] + "्").is_vyanjana()
        ):
            return self.get_savarna(code[0] + "्")
        if len(code) == 3 and code[1] == "त" and code[2] == "्":
            return [code[0], code[0] + "ँ"]
        if len(code) == 1 and self.get_varna(code[0]).is_svara():
            return self.get_savarna(code[0])
        if len(code) == 3 and code[2] == "्":
            start = code[0]
            stop = code[1] + code[2]

            i = self.maaheshwara_sutra.index(start)
            j = self.maaheshwara_sutra.index(stop)

            section = self.maaheshwara_sutra[i:j]

            it_letter = [
                x for x in section if len(x) == 2 and self.get_varna(x).is_vyanjana()
            ]

            for letter in it_letter:
                section.remove(letter)

            print(section)

            section = [x if x in self.varnas else x + "्" for x in section]

            extension = [
                self.get_savarna(x) for x in section if self.get_varna(x).is_svara()
            ]

            extension = [item for sublist in extension for item in sublist]

            section.extend(extension)

            return section

        return []


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

V = Varnamaalaa("akshara/resources/latest.csv", "akshara/resources/vividha.yml")

print(V.get_savarna("अ"))
print(V.get_savarna("त्"))
print(V.get_savarna("र्"))
print(V.get_savarna("ऋ"))
print(V.maaheshwara_sutra)
print(V.get_varna("क्").get_roopa())
print(V.expand("चु"))
print(V.expand("आत्"))
print(V.expand("आ"))
print(V.expand("हल्"))
print(V.expand("अल्"))
