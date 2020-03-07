from typing import List


class Matchup:
    """Model for a character's matcup."""

    def __init__(self, name: str):
        """
        Construct matchup object.

        :param name: `str` code name of the character
        """
        self.name = name
        self.title = "MISSING"
        self.overview = "MISSING"
        self.criticaltips = []
        self.counterpicks = "MISSING"
        self.bans = "MISSING"
        self.image = "MISSING"
        self.doclink = "MISSING"

    def set_title(self, t: str):
        """
        Set the title of the matchup.

        :param t: `str`
        """
        self.title = t

    def set_overview(self, o: str):
        """
        Set the overview of the matchup.

        :param o: `str`
        """
        self.overview = o

    def set_criticaltips(self, tips: List):
        """
        Set the on critical tips of the matchup.

        :param tips: `List`
        """
        self.criticaltips = tips

    def set_counterpicks(self, c: str):
        """
        Set the counterpick stages of the matchup.

        :param c: `str`
        """
        self.counterpicks = c

    def set_bans(self, b: str):
        """
        Set the banned stages of the matchup.

        :param b: `str`
        """
        self.bans = b

    def set_image(self, i: str):
        """
        Set the character image link of the matchup.

        :param i: `str`
        """
        self.image = i

    def set_doclink(self, l: str):
        """
        Set the google doc link of the matchup.

        :param l: `str`
        """
        self.doclink = l
