TASK_TRIGGERS = [
    "i need to",
    "i should",
    "i must",
    "remind me to",
    "i have to",
    "todo",
]


def extract_task(text):

    lower = text.lower()

    for trigger in TASK_TRIGGERS:

        if trigger in lower:

            task = lower.split(trigger, 1)[1].strip()

            return task

    return None