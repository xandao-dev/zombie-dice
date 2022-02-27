import random

DICES_FACES = {
    'green': ['shotgun'] * 1 + ['runner'] * 2 + ['brain'] * 3,
    'yellow': ['shotgun'] * 2 + ['runner'] * 2 + ['brain'] * 2,
    'red': ['shotgun'] * 3 + ['runner'] * 2 + ['brain'] * 1,
}
DICES_BOX = ['green'] * 6 + ['yellow'] * 4 + ['red'] * 3


def main():
    dices = pick_dices(3)
    rolls = roll_dices(dices)

    print(dices)
    print(rolls)


def pick_dices(n_of_dices: int) -> list:
    total_dices = len(DICES_BOX)
    if n_of_dices > total_dices:
        raise ValueError('Not enough dices')
    picked_dices = random.sample(DICES_BOX, n_of_dices)
    return picked_dices


def roll_dices(dices: list) -> list:
    return [random.choice(DICES_FACES[dice]) for dice in dices]


if __name__ == '__main__':
    main()
