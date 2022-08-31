from typing import List, Union


def is_english_sentence(sentence: str) -> bool:
    """The is_english_sentence method checks whether the sentece is a English sentence.
    Args:
        sentence (str)
    Returns:
        True if the sentence is English, False otherwise.
    """

    english_checker = lambda value: not (19968 <= ord(value) <= 40869)
    return all(map(english_checker, sentence))


def validate_sentence(sentence: str) -> Union[str, None]:
    """The validate_sentence method validates whether the sentence is English.
    Args:
        sentence (str)
    Returns:
        a str if the sentence is not a full English, None otherwise.
    """
    if not is_english_sentence(sentence.strip()):
        return sentence.strip()


def extract_mandarin(sentence: str) -> List[str]:
    """The extract_mandarin function extracts sentences that are not full English sentences.
    Args:
        sentence (str)
    Retunrs:
        a list
    """
    output = map(validate_sentence, sentence.split())
    return list(filter(lambda value: value is not None, output))
