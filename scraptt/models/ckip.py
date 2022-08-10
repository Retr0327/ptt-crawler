import pickle
from ..configs import ckip_path


def connect_ckip_drivers():
    """The connect_ckip_drivers functino connects to the ckip drivers.

    Returns:
        a tuple, containing CkipWordSegmenter and CkipPosTagger.
    """

    with open(ckip_path, "rb") as file:
        return pickle.load(file)
