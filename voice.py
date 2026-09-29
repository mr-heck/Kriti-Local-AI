import pyttsx3
import re
import threading

engine = pyttsx3.init()

# ==========================
# SELECT FEMALE VOICE
# ==========================

selected = False

for voice in engine.getProperty("voices"):

    print("VOICE FOUND:", voice.name)

    if "zira" in voice.name.lower():

        engine.setProperty(
            "voice",
            voice.id
        )

        print("USING VOICE:", voice.name)

        selected = True
        break

if not selected:
    print("WARNING: Zira not found, using default voice.")

# ==========================
# VOICE SETTINGS
# ==========================

engine.setProperty("rate", 180)
engine.setProperty("volume", 1.0)

voice_lock = threading.Lock()

# ==========================
# CLEAN TEXT
# ==========================

def clean_for_voice(text):

    text = str(text)

    emojis = [
        "😂", "🤣", "😊",
        "❤️", "💜", "🧡",
        "🌿", "🐦"
    ]

    for emoji in emojis:
        text = text.replace(emoji, "")

    # remove markdown symbols
    text = text.replace("*", "")
    text = text.replace("#", "")
    text = text.replace("_", "")

    # remove strange unicode symbols
    text = re.sub(r"[^\w\s.,!?']", "", text)

    # remove repeated punctuation
    text = re.sub(r"\.{2,}", ".", text)

    return text.strip()

# ==========================
# SPEAK
# ==========================

def speak(text):

    text = clean_for_voice(text)

    if not text:
        return

    with voice_lock:

        try:

            engine.stop()

            engine.say(text)

            engine.runAndWait()

        except Exception as e:

            print("[VOICE ERROR]", e)