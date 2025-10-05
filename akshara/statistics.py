"""A module for statistical analysis of text data"""

from dataclasses import dataclass

from akshara.varnakaarya import get_vinyaasa
from akshara.varna import Varnamaalaa

vn = Varnamaalaa()


@dataclass
class TextStatistics:
    """A class to hold statistical data about text"""

    text: str

    @property
    def characters(self) -> list[str]:
        """Returns a list of characters in the text"""
        return get_vinyaasa(self.text)

    @property
    def num_characters(self) -> int:
        """Returns the number of characters in the text"""
        return len(self.characters)

    @property
    def all_character_frequency(self) -> dict[str, int]:
        """Returns a dictionary with character frequencies"""
        frequency = {}
        for char in self.characters:
            if char in frequency:
                frequency[char] += 1
            else:
                frequency[char] = 1
        return frequency

    @property
    def swara_frequency(self) -> dict[str, int]:
        """Returns a dictionary with swara (vowel) frequencies"""

        frequency = {}
        for char in self.characters:
            if char in vn.svara or char in vn.anunaasika_svara:
                if char in frequency:
                    frequency[char] += 1
                else:
                    frequency[char] = 1
        return frequency

    @property
    def vyanjana_frequency(self) -> dict[str, int]:
        """Returns a dictionary with vyanjana (consonant) frequencies"""

        frequency = {}
        for char in self.characters:
            if char in vn.vyanjana:
                if char in frequency:
                    frequency[char] += 1
                else:
                    frequency[char] = 1
        return frequency

    @property
    def num_sentences(self) -> int:
        """Returns the number of sentences in the text"""
        sentence_endings = {".", "।", "॥", "!", "?"}
        count = sum(1 for char in self.text if char in sentence_endings)
        if self.text and self.text[-1] not in sentence_endings:
            count += 1  # Count the last sentence if it doesn't end with a punctuation
        return count


def main():
    """Main function to demonstrate the usage of TextStatistics class"""

    sample_text = "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन।"
    stats = TextStatistics(sample_text)
    print("Text:", stats.text)
    print("Number of characters:", stats.num_characters)
    print("Character frequencies:", stats.all_character_frequency)
    print("Swara frequencies:", stats.swara_frequency)
    print("Vyanjana frequencies:", stats.vyanjana_frequency)


if __name__ == "__main__":
    main()
