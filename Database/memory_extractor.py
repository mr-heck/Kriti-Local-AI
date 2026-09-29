import json
import re

from llm import ask_llm


def extract_memory(message):

    text = message.strip()
    lower = text.lower()

    # =====================================
    # IDENTITY
    # =====================================

    patterns = [

        (r"my name is (.+)", "Name is {}"),
        (r"i am (.+)", "Is {}"),
        (r"i'm (.+)", "Is {}"),

        # Preferences
        (r"i like (.+)", "Likes {}"),
        (r"i love (.+)", "Loves {}"),
        (r"i enjoy (.+)", "Enjoys {}"),
        (r"i prefer (.+)", "Prefers {}"),

        # Favorites
        (r"my favorite game is (.+)", "Favorite game is {}"),
        (r"my favourite game is (.+)", "Favorite game is {}"),

        (r"my favorite movie is (.+)", "Favorite movie is {}"),
        (r"my favourite movie is (.+)", "Favorite movie is {}"),

        (r"my favorite book is (.+)", "Favorite book is {}"),
        (r"my favourite book is (.+)", "Favorite book is {}"),

        (r"my favorite song is (.+)", "Favorite song is {}"),
        (r"my favourite song is (.+)", "Favorite song is {}"),

        # Goals
        (r"i want to become (.+)", "Wants to become {}"),
        (r"i want to be (.+)", "Wants to become {}"),
        (r"my dream is to become (.+)", "Dreams of becoming {}"),
        (r"my goal is to become (.+)", "Goal is becoming {}"),

        # Learning
        (r"i am learning (.+)", "Learning {}"),
        (r"i'm learning (.+)", "Learning {}"),
        (r"i study (.+)", "Studies {}"),

        # Skills
        (r"i use (.+)", "Uses {}"),
        (r"i know (.+)", "Knows {}"),

        # Projects
        (r"i am building (.+)", "Building {}"),
        (r"i'm building (.+)", "Building {}"),
        (r"i built (.+)", "Built {}"),
        (r"i created (.+)", "Created {}"),

        # Location
        (r"i live in (.+)", "Lives in {}"),
        (r"i am from (.+)", "Is from {}"),

        # Education
        (r"i study at (.+)", "Studies at {}"),

        # Personal Facts
        (r"i am vegan", "Is vegan"),
        (r"i am vegetarian", "Is vegetarian"),
        (r"i am pure veg", "Is pure vegetarian"),
    ]

    # =====================================
    # FAST PYTHON EXTRACTION
    # =====================================

    for pattern, template in patterns:

        match = re.search(
            pattern,
            lower,
            re.IGNORECASE
        )

        if match:

            if match.groups():

                extracted = match.group(1).strip()

                summary = template.format(
                    extracted
                )

            else:

                summary = template

            print("[FAST EXTRACTION]")
            print(summary)

            return summary

    # =====================================
    # LLM FALLBACK
    # =====================================

    print("[LLM EXTRACTION FALLBACK]")

    prompt = f"""
You are a memory extractor.

Convert the message into a short factual memory.

Rules:

- Third person
- Short
- Preserve meaning
- No extra explanation

Return ONLY JSON.

Example:

{{
    "summary": "Wants to become a game developer"
}}

Message:

{text}
"""

    try:

        response = ask_llm(prompt)

        data = json.loads(response)

        return data.get(
            "summary",
            ""
        )

    except Exception as e:

        print(
            f"Memory extractor error: {e}"
        )

        return text