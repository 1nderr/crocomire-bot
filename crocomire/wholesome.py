from random import choice, seed
from discord import Member

comp_path: str = "databases/compliments"


def give_compliment(user: Member) -> str:
    c: str = get_compliment()[:-1]
    return "{} {}!".format(user.mention, c)


def get_compliment():
    with open(comp_path, "r") as f:
        seed()
        return choice(f.readlines())
