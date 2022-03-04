import random
from typing import List

# Constants
MIN_NUMBER_OF_PLAYERS = 2
MAX_NUMBER_OF_PLAYERS = 8
MIN_NAME_LENGTH = 3
MAX_NAME_LENGTH = 13
MAX_SCORE = 13
INITIAL_AMOUNT_OF_DICES = 13
DICES_TO_ROLL = 3
DICES_FACES = {
    "green": ["shotgun"] * 1 + ["runner"] * 2 + ["brain"] * 3,
    "yellow": ["shotgun"] * 2 + ["runner"] * 2 + ["brain"] * 2,
    "red": ["shotgun"] * 3 + ["runner"] * 2 + ["brain"] * 1,
}
COLORS = {
    # ANSI Escape Sequences
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "RED": "\033[91m",
    "BLUE": "\033[94m",
    "PURPLE": "\033[95m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
    "END": "\033[0m",
}


class Dice:
    def __init__(self, color: str):
        self.color = color
        self.face = ""

    def roll(self):
        self.face = random.choice(DICES_FACES[self.color])

    def reset(self):
        self.face = ""

    def __str__(self):
        return self.face

    def __repr__(self):
        return f"Dice('{self.color}', '{self.face}')"


class Player:
    def __init__(self, name: str):
        self.name = name
        self.score = 0

    def add_score(self, score: int) -> None:
        self.score += score

    def reset_score(self) -> None:
        self.score = 0

    def __str__(self):
        return f"{self.name} has eaten {self.score} brains!"

    def __repr__(self):
        return f"Player('{self.name}', {self.score})"


# Variables
dices_box = [Dice("green")] * 6 + [Dice("yellow")] * 4 + [Dice("red")] * 3


def main():
    introduce_game()
    n_of_players = get_valid_number_of_players()
    players_name = get_valid_players_name(n_of_players)
    players = [Player(name) for name in players_name]
    introduce_players(players_name)

    print(dices_box)
    dices = pick_dices(DICES_TO_ROLL)
    rolls = roll_dices(dices)
    print(dices_box)

    print(players)
    print(dices)
    print(rolls)


def introduce_game() -> None:
    boldAndUnderline = COLORS["BOLD"] + COLORS["UNDERLINE"]
    print(
        f"""
{boldAndUnderline}
Welcome to 🧟 {COLORS["GREEN"]}Zombie{COLORS["END"]}{boldAndUnderline} 🎲 Dice!
{COLORS["END"]}
"""
    )


def get_valid_number_of_players() -> int:
    while True:
        try:
            try:
                n_of_players = int(input("How many 🧟 zombies will play (2-8)? "))
            except ValueError:
                print("You must enter a number of players!")
                raise ValueError("Not a valid number of players")

            if n_of_players < MIN_NUMBER_OF_PLAYERS:
                print(f"You need at least {MIN_NUMBER_OF_PLAYERS} zombies!")
                raise ValueError("Too few players")
            if n_of_players > MAX_NUMBER_OF_PLAYERS:
                print(f"You can play at most {MAX_NUMBER_OF_PLAYERS} zombies!")
                raise ValueError("Too many players")
        except ValueError:
            continue
        else:
            break
    return n_of_players


def get_valid_players_name(n_of_players: int) -> list:
    players = []
    print(f"Insert each 🧠 brain eater name below. Empty for generic name.")

    for index in range(n_of_players):
        readable_index = index + 1
        name = input(f"Zombie {readable_index}: ").strip()

        while True:
            if name in players:
                print(f"{name} is already in the game! Try another one.")
            elif len(name) < MIN_NAME_LENGTH:
                print(f"Name too short! It must be at least {MIN_NAME_LENGTH} characters long.")
            elif len(name) > MAX_NAME_LENGTH:
                print(f"Name too long! It must be at most {MAX_NAME_LENGTH} characters long.")
            else:
                break
            name = input(f"Zombie {readable_index}: ").strip()

        if name == "":
            name = f"Zombie {readable_index}"
        players.append(name)
    return players


def introduce_players(players_name: List[str]) -> None:
    players_string = COLORS["RED"] + ", ".join(players_name[:-1]) + f" and {players_name[-1]}" + COLORS["END"]
    print(f"🧟 Grrr!!! Have fun {players_string}")


def pick_dices(n_of_dices: int) -> list:
    total_dices = len(dices_box)
    if n_of_dices > total_dices:
        raise ValueError("Unavailable amount of dices!")
    picked_dices = random.sample(dices_box, n_of_dices)
    for dice in picked_dices:
        dices_box.remove(dice)
    return picked_dices


def return_dices(dices: list) -> None:
    dices_box.extend(dices)
    assert len(dices_box) > INITIAL_AMOUNT_OF_DICES, "More dices than existing amount!"


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
        exit(0)
    except Exception as e:
        print(f"\nSomething went wrong. Error: {e}")
        exit(0)
