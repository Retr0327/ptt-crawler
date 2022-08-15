from typing import List
from dataclasses import dataclass
from .....models import connect_ckip_drivers


@dataclass
class CKIPTransformer:
    """
    The Transformer object segments the sentences in a list.
    """

    sentence_list: List[str]

    def __post_init__(self) -> None:
        self.ws_driver, self.pos_driver = connect_ckip_drivers()

    def remove_empty_string(self, sentence_list: List[str]) -> List[str]:
        return list(filter(lambda value: value is not "", sentence_list))

    def pack_ws_pos_sentece(self, ws_pos_pair: tuple) -> List[tuple]:
        """The pack_ws_pos_sentece method packs both words and thier part-of-speech to a pair.

        Args:
            ws_pos_pair (tuple): the pair of a word and its corresponding part-of-speech
        Returns:
            a list of tuples: [
                ('我', 'Nh'),
                ('喜歡', 'VK'),
                ('程式', 'Na')
            ]
        """

        sentence_ws, sentence_pos = ws_pos_pair
        assert len(sentence_ws) == len(sentence_pos)
        return list(
            map(lambda word_pos_pair: word_pos_pair, zip(sentence_ws, sentence_pos))
        )

    def transform(self) -> List[List[tuple]]:
        """The transform method transforms the sentences in a list to word segmentation and part-of-speech results.

        Returns:
            an empty string if there is no comment, a list of lists of tuples otherwise: [
                [('我', 'Nh'), ('喜歡', 'VK'), ('程式', 'Na')],
                [('好', 'Dfa'), ('想', 'VE'), ('睡覺', 'VA')]
            ]
        """
        invalid_list = not self.sentence_list or all(
            [value == "" for value in self.sentence_list]
        )

        if invalid_list:
            return self.sentence_list

        filtered_list = self.remove_empty_string(self.sentence_list)
        ws_pipeline = self.ws_driver(filtered_list, use_delim=True)
        pos_pipeline = self.pos_driver(ws_pipeline, use_delim=True)
        return list(map(self.pack_ws_pos_sentece, zip(ws_pipeline, pos_pipeline)))
