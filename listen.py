import speech_recognition as sr


def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

        audio = recognizer.listen(source)

    languages = [
        "en-IN",
        "mr-IN",
        "hi-IN"
    ]

    for language in languages:

        try:

            text = recognizer.recognize_google(
                audio,
                language=language
            )

            print("You said:", text)

            return text

        except:
            continue

    return ""