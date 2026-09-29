def analyze_memory(summary):

    text = summary.lower()

    # ==========================
    # HIGH IMPORTANCE
    # ==========================

    high_importance = [

        "dream",
        "goal",
        "career",
        "ambition",
        "life goal",
        "project",
        "startup",
        "business",
        "internship",
        "exam",
        "test",
        "deadline",
        "birthday",
        "name",
        "college",
        "university",
        "degree",
        "education"
    ]

    # ==========================
    # MEDIUM IMPORTANCE
    # ==========================

    medium_importance = [

        "favorite",
        "favourite",
        "love",
        "like",
        "hobby",
        "interest",
        "skill",
        "learning",
        "unity",
        "blender",
        "krita",
        "game",
        "movie",
        "book",
        "music"
    ]

    # ==========================
    # CATEGORY DETECTION
    # ==========================

    category_map = {

        "career": [
            "career",
            "job",
            "profession",
            "developer",
            "internship",
            "work"
        ],

        "education": [
            "college",
            "university",
            "study",
            "exam",
            "test",
            "degree"
        ],

        "project": [
            "project",
            "building",
            "created",
            "developing"
        ],

        "hobby": [
            "game",
            "movie",
            "book",
            "music",
            "hobby",
            "interest"
        ],

        "skill": [
            "unity",
            "blender",
            "krita",
            "python",
            "c#",
            "skill",
            "learning"
        ],

        "personal facts": [
            "name",
            "birthday",
            "vegan",
            "vegetarian",
            "age",
            "family"
        ]
    }

    # ==========================
    # CATEGORY
    # ==========================

    category = "general"

    for cat, words in category_map.items():

        for word in words:

            if word in text:

                category = cat
                break

        if category != "general":
            break

    # ==========================
    # IMPORTANCE
    # ==========================

    importance = 5

    for word in high_importance:

        if word in text:

            importance = 9
            break

    if importance == 5:

        for word in medium_importance:

            if word in text:

                importance = 7
                break

    # ==========================
    # SHOULD STORE
    # ==========================

    should_store = True

    short_garbage = [

        "hello",
        "hi",
        "hey",
        "thanks",
        "thank you",
        "good morning",
        "good night",
        "bye"
    ]

    if text.strip() in short_garbage:

        should_store = False

    return {

        "should_store": should_store,
        "category": category,
        "importance": importance
    }