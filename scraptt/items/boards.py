from pydantic import BaseModel


class BoardItem(BaseModel):
    """
    The BoardItem object keeps track of an item in inventory.
    """

    name: str
