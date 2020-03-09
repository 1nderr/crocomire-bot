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
        Set the critical tips of the matchup.

        :param tips: `List`
        """
        self.criticaltips = tips

    def add_criticaltip(self, t: str):
        """
        Append the given tip to the matchup's tips.

        :param t: `str`
        """
        if self.criticaltips == ["MISSING"]:
            self.criticaltips[0] = t
        else:
            self.criticaltips.append(t)

    def replace_criticaltip(self, t: str, i: int):
        """
        Replace the tip at the given index.

        :param t: `str`
        :param i: `int`
        """
        if self.criticaltips == ["MISSING"]:
            self.criticaltips[0] = t
        else:
            self.criticaltips[i] = t

    def remove_criticaltip(self, i: int):
        """
        Remove the tip at the given index.

        :param i: `int`
        """
        self.criticaltips.pop(i)

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
