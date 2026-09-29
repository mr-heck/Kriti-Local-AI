from pathlib import Path

EMOTION_DIR = Path(__file__).parent / "emotions"

EMOTION_CATEGORIES = [
    "happy",
    "excited",
    "proud",
    "sad",
    "anxious",
    "frustrated",
    "angry",
    "tired",
    "lonely",
    "confused"
]


def load_word_list(filename):

    path = EMOTION_DIR / filename

    if not path.exists():
        print(f"[EMOTION FILE MISSING] {filename}")
        return set()

    try:

        with open(path, "r", encoding="utf-8") as file:

            return {
                line.strip().lower()
                for line in file
                if line.strip()
                and not line.startswith("#")
            }

    except Exception as error:

        print(f"[EMOTION LOAD ERROR] {filename}: {error}")
        return set()


def load_emotion_data():

    emotions = {}

    for emotion in EMOTION_CATEGORIES:

        emotions[emotion] = load_word_list(
            f"{emotion}.txt"
        )

    print(
        f"[EMOTIONS LOADED] "
        f"{len(emotions)} categories"
    )

    return emotions