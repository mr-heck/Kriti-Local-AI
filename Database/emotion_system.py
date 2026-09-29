import re

from Database.emotion_loader import load_emotion_data

EMOTIONS = load_emotion_data()

EMOTION_TO_SENTIMENT = {

    "happy": "positive",
    "excited": "positive",
    "proud": "positive",

    "sad": "negative",
    "anxious": "negative",
    "frustrated": "negative",
    "angry": "negative",
    "tired": "negative",
    "lonely": "negative",

    "confused": "neutral",
    "neutral": "neutral"
}


INTENSIFIERS = {
    "very": 0.15,
    "really": 0.15,
    "extremely": 0.30,
    "super": 0.20,
    "totally": 0.20,
    "completely": 0.30,
    "so": 0.10
}


def tokenize(text):

    return re.findall(
        r"\b[\w']+\b",
        text.lower()
    )


def analyze_emotion(text):

    words = tokenize(text)

    scores = {
        emotion: 0
        for emotion in EMOTIONS
    }

    intensity_bonus = 0

    for word in words:

        if word in INTENSIFIERS:
            intensity_bonus += INTENSIFIERS[word]

        for emotion in scores:

            if word in EMOTIONS[emotion]:
                scores[emotion] += 1

    highest_score = max(scores.values())

    if highest_score == 0:

        emotion = "neutral"

        return {
            "emotion": emotion,
            "sentiment": "neutral",
            "intensity": 0.0
        }

    emotion = max(
        scores,
        key=scores.get
    )

    sentiment = EMOTION_TO_SENTIMENT.get(
        emotion,
        "neutral"
    )

    intensity = min(
        1.0,
        (scores[emotion] * 0.25)
        + intensity_bonus
    )

    return {

        "emotion": emotion,

        "sentiment": sentiment,

        "intensity": round(
            intensity,
            2
        )
    }