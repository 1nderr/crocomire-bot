from random import choice, seed
from typing import List

comp_path: str = "databases/compliments"
smiles: List = [":)", "^_^", ":D", ":-)",
                "(◠﹏◠✿)", "●‿●", "ヽ(^◇^*)/",
                "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧", "(づ｡◕‿‿◕｡)づ",
                "(ᵔᴥᵔ)", "(~˘▾˘)~", "(^_^)"]


def give_compliment(user: str) -> str:
    c: str = get_compliment()[:-2]
    e: str = choice(smiles)
    return "{} {} {}".format(user, c, e)


def get_compliment():
    with open(comp_path, "r") as f:
        seed()
        return choice(f.readlines())
