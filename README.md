# Kriti — Local AI Companion

Kriti is a local AI companion that I'm building from scratch as an experiment in combining **LLMs, memory, context, emotions, voice, and character systems** into a single interactive software character.

The longer-term goal is to evolve Kriti into a **desktop-pet AI** and use what I learn from the project to explore how similar systems could be applied to **game development and AI-driven game characters**.

This is an ongoing personal project, so the architecture and features are still evolving.

---

## Current Progress

Kriti is already able to go beyond a basic question-and-answer chatbot.

### 💬 Conversation

Kriti can have conversations using a **locally running LLM**, allowing the core AI interaction to work without relying entirely on cloud-based AI services.

### 🧠 Persistent Memory

Kriti has a memory system that can:

* Detect potentially useful information from conversations
* Extract memories from natural conversation
* Assign importance to memories
* Store relevant information persistently
* Retrieve previous memories when they are useful
* Use retrieved memories as context for future conversations

The goal is to make conversations feel connected instead of treating every message as a completely isolated interaction.

### 🎭 Emotion System

Kriti also has a separate emotion-processing system.

Instead of asking the LLM to determine every emotional state, the current system uses a dedicated non-LLM approach to detect conversational emotion and tone.

This allows emotion to become another piece of context that can influence how Kriti responds.

### 🎙️ Voice Interaction

Kriti supports voice input and voice output, allowing interaction through speech instead of relying entirely on text.

### 🧩 Personality & Character System

Kriti has her own personality and character configuration that is kept separate from the core language model.

This makes it possible to modify the character without rebuilding the entire AI system.

### 🖥️ Local Interface

The project includes a desktop/web-based interface for interacting with Kriti.

The interface and backend are being developed separately so that the underlying AI systems can eventually support different visual implementations.

---

## General Architecture

The project is being built as a collection of independent systems rather than putting everything into a single LLM prompt.

A simplified view is:

```text
                    User
                      │
                      ▼
              ┌──────────────┐
              │  Interaction │
              └──────┬───────┘
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
   ┌─────────────┐       ┌─────────────┐
   │   Emotion   │       │   Memory    │
   │   System    │       │   System    │
   └──────┬──────┘       └──────┬──────┘
          │                     │
          └──────────┬──────────┘
                     ▼
              ┌─────────────┐
              │    Context  │
              └──────┬──────┘
                     ▼
              ┌─────────────┐
              │  Local LLM  │
              └──────┬──────┘
                     ▼
              ┌─────────────┐
              │ Personality │
              │  & Response │
              └──────┬──────┘
                     ▼
                  Kriti
```

The architecture will continue changing as new systems are added and existing ones are improved.

---

## Technology

Current technologies and tools include:

* **Python**
* **Ollama**
* **Local LLMs**
* **SQLite**
* **Tkinter / Web-based UI**
* **Voice input & text-to-speech**
* Modular Python-based backend systems

The exact models and implementation details may change as development continues.

---

## Why I'm Building It

The main purpose of Kriti isn't simply to build another chatbot.

I'm interested in understanding how different systems can work together to create a software character that has:

* Memory
* Context
* Emotional state
* Personality
* Voice
* Persistent interaction

I'm also particularly interested in **local AI**, where these systems can run on the user's own hardware rather than requiring every interaction to be sent to a remote service.

---

## Future Direction

### 🖥️ Desktop Pet AI

The next major direction is turning Kriti into a more complete **desktop-pet AI**.

The idea is for her to become a small interactive character that can live on the desktop, interact with the user, react to different situations, remember previous interactions, and eventually interact with parts of the computer environment.

---

### 🎮 AI for Game Development

This is the part I'm particularly interested in exploring long term.

I eventually want to build a **game prototype using a game engine** where a local LLM can work alongside traditional game systems to influence NPC behaviour and situations.

Instead of replacing normal game logic, the AI could provide another layer of interaction using information such as:

```text
Player Actions
      +
NPC Memory
      +
Current Situation
      +
Emotional State
      +
Previous Interactions
      ↓
Local AI
      ↓
Context-dependent Response
```

The goal is to experiment with game worlds where characters and situations can react more naturally to what the player actually does, rather than relying entirely on fixed dialogue and predetermined responses.

Kriti is currently my testing ground for understanding the underlying systems needed to explore this idea.

---

## Project Status

🚧 **Active Development**

Kriti is still an experimental project.

Some systems are functional, while others are being redesigned and expanded as I learn more about local LLMs, AI architecture, game development, and interactive character systems.

The project will probably change quite a lot before reaching its long-term form.

---

## Current Focus

Right now I'm mainly working on:

* Improving memory retrieval and context handling
* Expanding emotion detection
* Improving the interaction between memory, emotion and personality
* Building a better desktop interface
* Exploring the desktop-pet concept
* Learning how these systems could eventually translate into game development

---

## Long-Term Idea

The bigger idea behind Kriti is simple:

> **Explore how local AI can be used to create software characters and, eventually, more reactive game worlds.**

Kriti is the first experiment.

The eventual destination is much closer to **game development**.

---

## Creator

**Abhishek Kulkarni**

Computer Science student focused on:

* Game Development
* Unity & C#
* Game Art & Design
* Python
* AI for Interactive Experiences

This project is being developed as a personal exploration alongside my game-development work.
