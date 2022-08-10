import pickle
from typing import Tuple
from ..configs import ckip_path
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger


def connect_ckip_drivers() -> Tuple(CkipWordSegmenter, CkipPosTagger):
    """The connect_ckip_drivers functino connects to the ckip drivers.

    Returns:
        a tuple, containing CkipWordSegmenter and CkipPosTagger.
    """

    with open(ckip_path, "rb") as file:
        return pickle.load(file)
