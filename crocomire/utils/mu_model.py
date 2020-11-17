from typing import List


class Matchup:
    def __init__(self, name: str):
        self.name = name
        self.title = "MISSING"
        self.overview = "MISSING"
        self.criticaltips = []
        self.counterpicks = "MISSING"
        self.bans = "MISSING"
        self.image = "MISSING"
        self.doclink = "MISSING"

    def set_title(self, t: str):
        self.title = t

    def set_overview(self, o: str):
        self.overview = o

    def set_criticaltips(self, tips: List):
        self.criticaltips = tips

    def add_criticaltip(self, t: str):
        if self.criticaltips == ["MISSING"]:
            self.criticaltips[0] = t
        else:
            self.criticaltips.append(t)

    def replace_criticaltip(self, t: str, i: int):
        if self.criticaltips == ["MISSING"]:
            self.criticaltips[0] = t
        else:
            self.criticaltips[i] = t

    def remove_criticaltip(self, i: int):
        self.criticaltips.pop(i)

    def set_counterpicks(self, c: str):
        self.counterpicks = c

    def set_bans(self, b: str):
        self.bans = b

    def set_image(self, i: str):
        self.image = i

    def set_doclink(self, l: str):
        self.doclink = l
