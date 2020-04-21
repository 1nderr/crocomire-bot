from random import choice, seed, randint
from string import ascii_letters

meme_path: str = "databases/memes"
tubes_path: str = "databases/tubesmemes"


def get_tubes_meme():
    with open(tubes_path, "r") as f:
        seed()
        return choice(f.readlines())


def get_random_meme():
    with open(meme_path, "r") as f:
        seed()
        return choice(f.readlines())


def add_meme(meme: str):
    with open(meme_path, "a") as f:
        f.write("\n" + meme)


def generate_mash():
    return "".join([choice(list(ascii_letters)) for i in range(randint(30, 76))])
