from abc import ABC, abstractmethod


class Parser(ABC):
    """
    The Parser object processes the response and returns scraped data or more URLs to follow.
    """

    @abstractmethod
    def parse(self):
        """The parse method initiates the parsing processes."""
        pass
