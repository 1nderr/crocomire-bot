from random import choice, seed
from typing import List

comp_path: str = "databases/compliments"
smiles: List = ["<:IsaJoy:694729890993406025>", "<:IsaBlush1:694729891450454086>", "<:IsaBlush2:694729891152658432>",
                "<:IsaBlush3:694729890854993941>", "<:IsaCool:694729891446390804>", "<:IsaHeart:694729891324755979>"]


def give_compliment(user: str) -> str:
    c: str = get_compliment()[:-1]
    e: str = choice(smiles)
    return "{} {} {}".format(user, c, e)


def get_compliment():
    with open(comp_path, "r") as f:
        seed()
        return choice(f.readlines())
