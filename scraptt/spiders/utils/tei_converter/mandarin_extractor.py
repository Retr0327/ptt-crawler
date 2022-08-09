from typing import List, Union
from dataclasses import dataclass


@dataclass
class MandarinExtractor:
    """
    The MandarinExtractor object extracts sentences that are not full English sentences.
    """

    sentence: str

    def is_english_sentence(self, sentence: str) -> bool:
        """The is_english_sentence method checks whether the sentece is a English sentence.

        Args:
            sentence (str)
        Returns:
            True if the sentence is English, False otherwise.
        """
        english_checker = lambda value: not (19968 <= ord(value) <= 40869)
        return all(map(english_checker, sentence))

    def validate_sentence(self, sentence: str) -> Union[str, None]:
        """The validate_sentence method validates whether the sentence is English.

        Args:
            sentence (str)
        Returns:
            a str if the sentence is not a full English, None otherwise.
        """
        if not self.is_english_sentence(sentence.strip()):
            return sentence.strip()

    def extract(self) -> List[str]:
        output = map(self.validate_sentence, self.sentence.split())
        return list(filter(lambda value: value is not None, output))
