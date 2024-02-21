"""Module to perform sutra related tasks"""

from dataclasses import dataclass
import json
import os


@dataclass
class Sutra:
    """Class to represent a sutra"""

    adhyaya: int
    paada: int
    number: int
    text: str

    def __repr__(self):
        return f"{self.adhyaya}.{self.paada}.{self.number}: {self.text}"

    def __post_init__(self):
        if not isinstance(self.adhyaya, int):
            raise ValueError("Adhyaya should be an integer")
        if not isinstance(self.paada, int):
            raise ValueError("Paada should be an integer")
        if not isinstance(self.number, int):
            raise ValueError("Number should be an integer")
        if not isinstance(self.text, str):
            raise ValueError("Text should be a string")

        if self.adhyaya < 1 or self.adhyaya > 8:
            raise ValueError("Adhyaya should be between 1 and 8")

        if self.paada < 1 or self.paada > 4:
            raise ValueError("Paada should be between 1 and 4")

        if self.number < 1:
            raise ValueError("Number should be a positive integer")


def create_sutra_list(filename: os.PathLike):
    """Create a list of Sutra objects from a file"""

    with open(filename, "r", encoding="utf-8") as file:
        lines = json.load(file)

    return list(
        Sutra(int(data["a"]), int(data["p"]), int(data["n"]), data["s"])
        for data in lines["data"]
    )


def main():
    """Main function"""

    print(create_sutra_list("akshara/sutra/sutra.json"))


if __name__ == "__main__":

    main()
