import pickle
from pathlib import Path

# --------------------------------------------------------------------
# ckip path

pkg_path = Path("__file__").resolve().parent / "scraptt"
ckip_dir = pkg_path / "models"
ckip_path = ckip_dir / "ckip_drivers.pickle"


def download_ckip_drivers() -> None:
    """The download_ckip_drivers function downloads the ckip drivers, and saves
    them to a pickle file if the `ckip_drivers.pickle` does not exist.
    """

    NLP_MODEL = "bert-base"
    has_path = Path(ckip_path).exists()

    if not has_path:
        from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger

        drivers = (CkipWordSegmenter(model=NLP_MODEL), CkipPosTagger(model=NLP_MODEL))

        with open(rf"{ckip_path}", "wb") as file:
            pickle.dump(drivers, file)


# --------------------------------------------------------------------
# cookies setting

COOKIES = {"over18": "1"}
