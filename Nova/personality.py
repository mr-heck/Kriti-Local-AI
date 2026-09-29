import json


def load_personality():

    with open(
        "Nova/personality.json",
        "r",
        encoding="utf-8"
    ) as file:

        personality = json.load(file)

    return personality