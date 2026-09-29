import re

print("[MEMORY DETECTOR LOADED]")


MEMORY_PATTERNS = [

    # Identity
    "i am",
    "i'm",
    "my name is",
    "call me",
    "i am called",

    # Likes
    "i like",
    "i love",
    "i enjoy",
    "i prefer",
    "i am a fan of",
    "i really like",
    "i absolutely love",
    "i adore",
    "i am interested in",

    # Favorites
    "my favorite",
    "my favourite",
    "favorite game",
    "favourite game",
    "favorite movie",
    "favorite food",
    "favorite book",
    "favorite song",
    "favorite color",
    "favorite colour",

    # Goals
    "i want to",
    "i wish to",
    "my goal is",
    "my dream is",
    "i dream of",
    "i hope to",
    "i plan to",
    "i want to become",
    "i want to build",
    "i want to create",
    "my ambition is",

    # Skills
    "i know",
    "i can",
    "i use",
    "i work with",
    "i develop",
    "i create",
    "i code in",
    "i program in",

    # Learning
    "i am learning",
    "i'm learning",
    "i study",
    "i am studying",
    "currently learning",
    "i am practicing",

    # Projects
    "i am building",
    "i'm building",
    "i built",
    "i created",
    "my project",
    "i am working on",
    "i'm working on",

    # Hobbies
    "i play",
    "my hobby",
    "i enjoy playing",
    "in my free time",
    "i spend time",

    # Personal Facts
    "i live",
    "i am from",
    "i was born",
    "my birthday",
    "i am vegan",
    "i am vegetarian",
    "i am pure veg",

    # Relationships
    "my friend",
    "my sister",
    "my brother",
    "my mother",
    "my father",
    "my parents",
    "my family",

    # Education
    "i study at",
    "my college",
    "my university",
    "i am in",
    "i am a student",

    # Work
    "my job",
    "i work as",
    "my profession",
    "my career",

    # Gaming
    "my favorite game is",
    "i love playing",
    "i enjoy playing",
    "i play a lot of",

    # Movies
    "my favorite movie is",
    "i love watching",

    # Music
    "my favorite song is",
    "my favorite artist is",

    # Technology
    "i use unity",
    "i use blender",
    "i use unreal",
    "i use krita",
    "i use affinity"
]


BLOCKED_QUESTIONS = [

    "who am i",
    "do you know who i am",
    "what is my dream",
    "what are my dreams",
    "what game do i like",
    "what games do i like",
    "what do you remember about me",
    "show memories",
    "show memory",
    "list memories",
    "what is my favorite game",
    "what do i like",
    "what are my hobbies",
    "what is my goal"
]


SHORT_MESSAGES = [

    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon",
    "good evening",
    "good night",

    "thanks",
    "thank you",

    "ok",
    "okay",
    "cool",
    "nice",
    "great",

    "bye",
    "goodbye",

    "how are you",
    "what are you doing",

    "tell me a joke",
    "tell me something"
]


def detect_memory(message):

    print(f"[CHECKING] {message}")

    message_lower = message.lower().strip()

    # Block memory questions
    for question in BLOCKED_QUESTIONS:

        if question in message_lower:

            print("[BLOCKED QUESTION]")
            return False

    # Ignore short casual chat
    if message_lower in SHORT_MESSAGES:

        print("[SHORT MESSAGE]")
        return False

    # Fast keyword matching
    for keyword in MEMORY_PATTERNS:

        if keyword in message_lower:

            print("[FAST MEMORY DETECTED]")
            return True

    # Simple regex patterns

    regex_patterns = [

        r"my favorite .* is .*",
        r"my favourite .* is .*",
        r"i want to .*",
        r"i love .*",
        r"i like .*",
        r"i enjoy .*",
        r"i am learning .*",
        r"i study .*",
        r"i work .*",
        r"i use .*",
        r"i built .*",
        r"i created .*",
        r"i am building .*",
        r"i am from .*",
        r"i live in .*",
        r"my dream is .*",
        r"my goal is .*",
    ]

    for pattern in regex_patterns:

        if re.search(pattern, message_lower):

            print("[REGEX MEMORY DETECTED]")
            return True

    print("[NO MEMORY FOUND]")
    return False