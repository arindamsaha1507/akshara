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
        self.anunaasika = parts[6] == "अनुनासिकः\n"

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

    def is_ayogavaaha(self) -> bool:
        """Checks if varna is ayogavaaha"""
        return self.bheda == "अयोगवाहः"

    def is_anunaasika(self) -> bool:
        """Checks if varna is anunaasika"""
        return self.anunaasika


class Varnamaalaa:
    """Class describing the varnamaalaa"""

    def __init__(
        self,
        varna_file_path="resources/latest.csv",
        vividha_file_path="resources/vividha.yml",
    ) -> None:
        path = f"{str(os.path.dirname(__file__))}"
        varna_file_path = f"{path}/{varna_file_path}"
        vividha_file_path = f"{path}/{vividha_file_path}"
        with open(varna_file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        with open(vividha_file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        self.varnamaalaa = list(Varna(line) for line in lines)
        self.varnas = [x.get_roopa() for x in self.varnamaalaa]
        self.all_svaras = [x.get_roopa() for x in self.varnamaalaa if x.is_svara()]
        self.all_vyanjanas = [
            x.get_roopa() for x in self.varnamaalaa if x.is_vyanjana()
        ]
        self.svara = [
            x.get_roopa()
            for x in self.varnamaalaa
            if x.is_svara() and x.anunaasika is False and x.kaala != "प्लुतः"
        ]
        self.anunaasika_svara = [
            x.get_roopa()
            for x in self.varnamaalaa
            if x.is_svara() and x.anunaasika is True and x.kaala != "प्लुतः"
        ]
        self.vyanjana = [x.get_roopa() for x in self.varnamaalaa if x.is_vyanjana()]
        self.vyanjana_with_akaara = [x[0] for x in self.vyanjana]
        self.ayogavaaha = [x.get_roopa() for x in self.varnamaalaa if x.is_ayogavaaha()]

        self.maaheshwara_sutra = data["maaheshwara_sutra"]
        self.maatraa = data["maatraa"]
        self.sankhyaa = data["sankhyaa"]
        self.avasaana = [" ", "।", "॥", "-"]

        self.maatraa_to_svara = dict(zip(self.maatraa, self.svara[1:]))
        self.svara_to_maatraa = dict(zip(self.svara[1:], self.maatraa))

    def get_savarna(self, varna: str) -> list:
        """Returns savarnas of a varna

        Args:
            varna (str): Input varna

        Returns:
            list: List of savarnas
        """

        ref = list(x for x in self.varnamaalaa if x.get_roopa() == varna)

        assert len(ref) == 1, f"Expected 1 and only 1 varna to find savarnas. Got {ref}"

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

        assert (
            len(varna) == 1
        ), f"Expected 1 and only 1 varna to varna properties. Got {varna}"

        return varna[0]

    def expand(self, code: str) -> list:
        """Pratyaahaaragrahana or savarnagrahana

        Args:
            code (str): Pratyaahaara or savarnagraahi

        Returns:
            list: List of varna
        """

        assert len(code) <= 3, f"Varnasanketa {code} is too long"

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
