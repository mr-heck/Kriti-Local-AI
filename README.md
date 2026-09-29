# Kriti

Kriti is a local AI companion that I'm building from scratch.

The project started as an experiment to see how far I could take a local AI beyond simply sending a message to an LLM and getting a reply. I'm currently working on things like memory, context, emotions, voice interaction and personality as separate parts of the system.

The bigger idea is to eventually turn Kriti into a desktop-pet AI, and later use what I learn from this project for AI-driven systems in my game development work.

This is still very much a work in progress.

## What Kriti can do right now

Kriti can already have conversations with me using a locally running LLM.

She also has a persistent memory system. Instead of forgetting everything after a conversation ends, the system can identify potentially useful information, extract it, assign importance to it and store it. Relevant memories can then be retrieved and provided as context when they are useful in a later conversation.

I've also been working on a separate emotion system. At the moment, emotions are detected without making another LLM call for every response. The idea is to keep things like emotional state outside the main language model so that I have more control over how the character behaves.

Kriti can also:

* Use voice input and text-to-speech
* Maintain a custom personality
* Use previous memories as conversational context
* Detect conversational emotions and tone
* Run locally on my own machine
* Use separate systems for memory, emotion, personality and conversation
* Work through a desktop/web-based interface

## How I'm building it

One thing I'm trying to avoid is putting the entire character inside one huge prompt.

The LLM is mainly responsible for understanding the conversation and generating a response. Other parts of Kriti handle things such as memory, emotion and personality.

So, roughly, a conversation looks something like this:

```text
User message
     |
     +---- Memory system
     |
     +---- Emotion system
     |
     +---- Other context
     |
     v
   Local LLM
     |
     v
  Kriti's response
```

This structure is still changing as I work on the project. I'm experimenting with different ways of connecting these systems without making everything dependent on the LLM.

## Technologies

The project currently uses:

* Python
* Ollama
* Local LLMs
* SQLite
* Tkinter / web-based UI
* Voice input and text-to-speech

The exact model and implementation will probably change as the project develops.

## Why I'm building Kriti

I'm interested in the idea of software characters that can actually build some context over time instead of behaving like a completely new chatbot every time you open them.

Memory is one part of that.

Emotion, personality and the ability to react to previous interactions are other parts.

I'm also deliberately experimenting with local AI because I want to understand what can realistically be done on normal consumer hardware without sending every interaction to a cloud service.

## Where I want to take it

The first major goal is to turn Kriti into a proper desktop-pet AI.

I'd like her to eventually be able to exist directly on the desktop, interact with the user, react to things happening around her and make use of the computer environment in useful ways.

But the part I'm more interested in from a game-development perspective comes after that.

I eventually want to build a game prototype using a game engine where a local LLM can work alongside normal game systems.

For example, an NPC could have some combination of:

```text
Previous interactions
NPC memory
Current situation
Emotional state
Player actions
```

and that information could be used by a local AI to produce a more context-dependent response.

I'm not trying to replace traditional game logic with an LLM. I want to experiment with where local AI can actually add something useful to a game.

The goal is to see whether characters and situations can feel more reactive without having every possible interaction manually written beforehand.

Kriti is basically my testing ground for learning the systems that could eventually make that possible.

## Current status

Kriti is actively being developed.

Some parts are already working, while others are still being redesigned and improved. The architecture will probably change quite a few times as I learn more.

Right now I'm mainly working on:

* Improving memory retrieval
* Making context handling more useful
* Expanding emotion detection
* Improving personality and character behaviour
* Building the desktop-pet side of the project
* Understanding how these systems could eventually be used in games

## Long-term idea

Kriti started as a local AI companion project.

The longer-term goal is to explore the same ideas in game development and see what happens when AI characters have memory, context and emotional state that can actually affect how they interact with the player.

There is still a lot to figure out.

For now, I'm just building it and seeing where it goes.

---

Created by **Abhishek Kulkarni**

Game Development | Unity & C# | Python | Game Art & Design | AI for Interactive Experiences
