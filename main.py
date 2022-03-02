import random

MIN_NUMBER_OF_PLAYERS = 2
MAX_NUMBER_OF_PLAYERS = 8

DICES_FACES = {
    "green": ["shotgun"] * 1 + ["runner"] * 2 + ["brain"] * 3,
    "yellow": ["shotgun"] * 2 + ["runner"] * 2 + ["brain"] * 2,
    "red": ["shotgun"] * 3 + ["runner"] * 2 + ["brain"] * 1,
}
DICES_BOX = ["green"] * 6 + ["yellow"] * 4 + ["red"] * 3
DICES_TO_ROLL = 3


def main():
    n_of_players = get_valid_number_of_players()
    players = get_valid_players_name(n_of_players)
    dices = pick_dices(DICES_TO_ROLL)
    rolls = roll_dices(dices)

    print(players)
    print(dices)
    print(rolls)


def get_valid_number_of_players() -> int:
    while True:
        try:
            try:
                n_of_players = int(input("How many 🧟 zombies will play (2-8)? "))
            except ValueError:
                print("You must enter a number of players!\n")
                raise ValueError("Not a valid number of players")

            if n_of_players < MIN_NUMBER_OF_PLAYERS:
                print(f"You need at least {MIN_NUMBER_OF_PLAYERS} zombies!\n")
                raise ValueError("Too few players")
            if n_of_players > MAX_NUMBER_OF_PLAYERS:
                print(f"You can play at most {MAX_NUMBER_OF_PLAYERS} zombies!\n")
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
                print(f"{name} is already in the game! Try another one.\n")
                name = input(f"Zombie {readable_index}: ").strip()
            elif len(name) < 3:
                print("Name too short! Try again.\n")
                name = input(f"Zombie {readable_index}: ").strip()
            else:
                break

        if name == "":
            name = f"Zombie {readable_index}"
        players.append(name)
    return players


def pick_dices(n_of_dices: int) -> list:
    total_dices = len(DICES_BOX)
    if n_of_dices > total_dices:
        print("Not enough dices\n")
    picked_dices = random.sample(DICES_BOX, n_of_dices)
    return picked_dices


def roll_dices(dices: list) -> list:
    return [random.choice(DICES_FACES[dice]) for dice in dices]


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
        exit(0)
    except:
        print("Something went wrong")
        exit(0)
