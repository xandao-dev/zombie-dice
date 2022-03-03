import random

# Constants
MIN_NUMBER_OF_PLAYERS = 2
MAX_NUMBER_OF_PLAYERS = 8
MIN_NAME_LENGTH = 3
MAX_NAME_LENGTH = 12
DICES_TO_ROLL = 3
dices_faces = {
    "GREEN": ["shotgun"] * 1 + ["runner"] * 2 + ["brain"] * 3,
    "YELLOW": ["shotgun"] * 2 + ["runner"] * 2 + ["brain"] * 2,
    "RED": ["shotgun"] * 3 + ["runner"] * 2 + ["brain"] * 1,
}
colors = {
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

# Variables
dices_box = ["GREEN"] * 6 + ["YELLOW"] * 4 + ["RED"] * 3


def main():
    introduce_game()
    n_of_players = get_valid_number_of_players()
    players = get_valid_players_name(n_of_players)
    introduce_players(players)
    dices = pick_dices(DICES_TO_ROLL)
    rolls = roll_dices(dices)

    print(players)
    print(dices)
    print(rolls)


def introduce_game() -> None:
    boldAndUnderline = colors["BOLD"] + colors["UNDERLINE"]
    print(
        f"""
{boldAndUnderline}
Welcome to 🧟 {colors["GREEN"]}Zombie{colors["END"]}{boldAndUnderline} 🎲 Dice!
{colors["END"]}
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


def introduce_players(players: list):
    # list to string with comma delimiter
    players_string = colors["RED"] + ", ".join(players[:-1]) + f" and {players[-1]}" + colors["END"]
    print(f"🧟 Grrr!!! Have fun {players_string}")


def pick_dices(n_of_dices: int) -> list:
    total_dices = len(dices_box)
    if n_of_dices > total_dices:
        print("Not enough dices")
    picked_dices = random.sample(dices_box, n_of_dices)
    return picked_dices


def roll_dices(dices: list) -> list:
    return [random.choice(dices_faces[dice]) for dice in dices]


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
        exit(0)
    except:
        print("\nSomething went wrong")
        exit(0)
