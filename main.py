import random
from typing import List, Optional

# Constants
MIN_NUMBER_OF_PLAYERS = 2
MAX_NUMBER_OF_PLAYERS = 8
MIN_NAME_LENGTH = 3
MAX_NAME_LENGTH = 13
MAX_SCORE = 13
MAX_SHOOTERS_PER_TURN = 3
INITIAL_AMOUNT_OF_DICES = 13
N_OF_DICES_TO_ROLL = 3
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
ACTIONS = {
    "roll": {
        "description": f"[{COLORS['GREEN']}r{COLORS['END']}] to pick and roll 3 dices",
        "key": "r",
    },
    "finish": {
        "description": f"[{COLORS['RED']}f{COLORS['END']}] to finish my turn",
        "key": "f",
    },
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
        self.dices = []

    def reset(self):
        self.score = 0
        return_dices(self.dices)

    def __str__(self):
        return self.name

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
    player_turn(players[0])


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


def pick_dices(n_of_dices: int) -> List[Dice]:
    total_dices = len(dices_box)
    if n_of_dices > total_dices:
        raise ValueError("Unavailable amount of dices!")
    picked_dices = random.sample(dices_box, n_of_dices)
    for dice in picked_dices:
        dices_box.remove(dice)
    return picked_dices


def return_dices(dices: List[Dice]) -> None:
    dices_box.extend(dices)
    assert len(dices_box) > INITIAL_AMOUNT_OF_DICES, "More dices than existing amount!"


def start_game(players: List[Player]):
    # if someone reaches 13 points, the game ends and show the score
    # if a tie happens, this two players will play against each other 1 round
    print("The game has started!")


def game_round(players: List[Player]):
    for player in players:
        player_turn(player)


def player_turn(player: Player) -> None:
    brains = 0
    shooters = 0
    runners = 0

    print("═" * 100)
    print(f"{COLORS['BOLD']}It's your turn {player}{COLORS['END']} 🧟")
    valid_actions = [ACTIONS["roll"], ACTIONS["finish"]]
    while True:
        while True:
            key = input(f"{player}, {', '.join(action['description'] for action in valid_actions)}: ").strip().lower()
            action = get_valid_action(key, valid_actions)
            if action != None:
                break

        if action == ACTIONS["roll"]:
            result = roll_action(player, brains, shooters, runners)
            if not result["success"]:
                finish_action(player, 0)
            brains += result["brains"]
            shooters += result["shooters"]
            runners += result["runners"]
        elif action == ACTIONS["finish"]:
            finish_action(player, brains)
            break
        print("─" * 100)


def get_valid_action(key: str, valid_actions: list) -> Optional[dict]:
    for action in valid_actions:
        if key == action["key"]:
            return action
    print(f"Invalid action! Available actions: {', '.join(action['description'] for action in valid_actions)}")
    return None


def roll_action(player: Player, brains: int, shooters: int, runners: int) -> None:
    runners_to_roll_again = []
    dices = []

    # Compute runners of the player to roll again
    for dice in player.dices:
        if dice.face != "runner" or len(runners_to_roll_again) <= N_OF_DICES_TO_ROLL:
            continue
        print("We have some runners, rolling them again!")
        runners_to_roll_again.append(dice)
        player.dices.remove(dice)
    n_of_dices_to_pick = N_OF_DICES_TO_ROLL - len(runners_to_roll_again)

    # Pick dices to roll again, considering the number of runners
    try:
        dices = pick_dices(n_of_dices_to_pick)
    except ValueError:
        # FIXME: When we run out of dices in the box
        print("Dices over, returning brains to the box and storing score in a temporary variable")
        # for dice in picked_dices:
        #    if dice.face == "brain":
        #        picked_dices.remove(dice)
        #        return_dices([dice])

    # Show picked dices
    print(f"🤌🎲 Picked {len(dices)} dices: ", end="")
    for dice in dices:
        if dice.color == "red":
            print(f"{COLORS['RED']}{dice.color} dice{COLORS['END']}; ", end="")
        elif dice.color == "yellow":
            print(f"{COLORS['YELLOW']}{dice.color} dice{COLORS['END']}; ", end="")
        elif dice.color == "green":
            print(f"{COLORS['GREEN']}{dice.color} dice{COLORS['END']}; ", end="")
    print("")

    # Show runners to roll again
    if len(runners_to_roll_again) > 0:
        print(f"🏃 You have {len(runners_to_roll_again)} runners to roll again: ", end="")
        for dice in runners_to_roll_again:
            if dice.color == "red":
                print(f"{COLORS['RED']}{dice.color} dice{COLORS['END']}; ", end="")
            elif dice.color == "yellow":
                print(f"{COLORS['YELLOW']}{dice.color} dice{COLORS['END']}; ", end="")
            elif dice.color == "green":
                print(f"{COLORS['GREEN']}{dice.color} dice{COLORS['END']}; ", end="")
        print("")

    # Extend the picked dices to the dices that will be rolled again
    dices.extend(runners_to_roll_again)
    # Add dices to the player's hand
    player.dices.extend(dices)

    # Roll the dices and compute the points
    for dice in dices:
        dice.roll()
        if dice.face == "brain":
            brains += 1
        elif dice.face == "shooter":
            shooters += 1
        elif dice.face == "runner":
            runners += 1

    # Show the rolled dices
    print(f"✊🎲 You rolled: ", end="")
    for dice in dices:
        if dice.color == "red":
            print(
                f"{COLORS['RED']}{dice.color} dice{COLORS['END']} -> {COLORS['BOLD']}{dice.face}{COLORS['END']}; ",
                end="",
            )
        elif dice.color == "yellow":
            print(
                f"{COLORS['YELLOW']}{dice.color} dice{COLORS['END']} -> {COLORS['BOLD']}{dice.face}{COLORS['END']}; ",
                end="",
            )
        elif dice.color == "green":
            print(
                f"{COLORS['GREEN']}{dice.color} dice{COLORS['END']} -> {COLORS['BOLD']}{dice.face}{COLORS['END']}; ",
                end="",
            )
    print("")

    # Stop if the player got 3 shooters
    if shooters >= MAX_SHOOTERS_PER_TURN:
        print("Busted, you got to many shooters")
        return {"success": False}

    print(f"Your current score is {brains + player.score}")
    return {"success": True, "brains": brains, "shooters": shooters, "runners": runners}


def finish_action(player: Player, add_score: int) -> None:
    print(f"{player} you have {add_score + player.score} points!")
    player.score += add_score


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
        exit(0)
    except Exception as e:
        print(f"\nSomething went wrong. Error: {e}")
        exit(0)
