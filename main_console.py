import json
from pathlib import Path


class Nova:
    def __init__(self):
        personality_path = Path("Nova/personality.json")

        with open(personality_path, "r", encoding="utf-8") as file:
            self.personality = json.load(file)

        self.name = self.personality["name"]

    def greet(self):
        print(f"\n{self.name}: Hello Abhishek!")
        print(f"{self.name}: I am your {self.personality['role']}.\n")

    def chat(self):
        self.greet()

        while True:
            user_input = input("You: ")

            if user_input.lower() in ["exit", "quit", "bye"]:
                print(f"{self.name}: Goodbye Abhishek!")
                break

            elif "name" in user_input.lower():
                print(f"{self.name}: My name is {self.name}.")

            elif "creator" in user_input.lower():
                print(f"{self.name}: I was created by {self.personality['creator']}.")

            elif "traits" in user_input.lower():
                traits = ", ".join(self.personality["traits"])
                print(f"{self.name}: My traits are {traits}.")

            else:
                print(f"{self.name}: That's interesting. Tell me more.")


if __name__ == "__main__":
    nova = Nova()
    nova.chat()