print("PYWEBVIEW_DEMO.PY LOADED")
import os
import sys
import time
# ==========================================
# FIND AI_HQ_NOVA ROOT
# ==========================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import threading
import webview

from llm import ask_llm
from listen import listen
from voice import speak
from Database.emotion_system import analyze_emotion
from Database.memory_detector import detect_memory
from Database.memory_extractor import extract_memory
from Database.memory_analyzer import analyze_memory
from Database.memory import (
    init_db,
    get_all_memories_text,
    get_relevant_memories,
    save_memory,
    save_chat_message,
    get_recent_chat
)


# ==========================================
# KRITI PERSONALITY
# ==========================================

SYSTEM_PROMPT = """
You are Kriti.

You are a cute AI companion.

Personality:
- playful
- bold
- slightly naughty
- teasing
- creative
- supportive
- emotionally warm

Creator:
Abhishek Kulkarni

Never claim to be ChatGPT.
Never mention OpenAI.

Speak naturally.

Keep replies concise.
Usually respond in 2-5 sentences.
Avoid long essays unless the user specifically asks.

If the user asks who they are, what they like,
their goals, dreams, projects or memories,
use the memory section provided below.

Do not invent memories.

If no memory exists, politely say you don't know yet.
"""

# ==========================================
# PYTHON API
# ==========================================

class KritiPythonAPI:

    def __init__(self, window):
        self.window = window

    def on_user_message(self, message):

        print(f"[Python] Received user message: {message}")

        threading.Thread(
            target=self._generate_ai_response,
            args=(message,),
            daemon=True
        ).start()

    def _generate_ai_response(self, user_text):

        print("[GENERATE CALLED]")
        print(user_text)
# ==========================
# EMOTION ANALYSIS
# ==========================

        emotion_data = analyze_emotion(user_text)

        print(
            f"[EMOTION] "
            f"{emotion_data['emotion']} | "
            f"{emotion_data['sentiment']} | "
            f"{emotion_data['intensity']}"
        )
        self.window.evaluate_js(
            "setStatus('Thinking')"
        )

        try:

            # ==========================
            # MEMORY PIPELINE
            # ==========================

            try:

                t1 = time.time()

                has_memory = detect_memory(user_text)

                print(f"[DETECTOR TIME] {time.time() - t1:.2f} sec")

                if has_memory:

                            print("[DETECTOR] True")

                            t2 = time.time()

                            summary = extract_memory(user_text)

                            print(f"[EXTRACTOR TIME] {time.time() - t2:.2f} sec")
                            print(f"[SUMMARY] {summary}")

                            t3 = time.time()

                            analysis = analyze_memory(summary)

                            print(f"[ANALYZER TIME] {time.time() - t3:.2f} sec")
                            print(f"[ANALYSIS] {analysis}")

                            if analysis.get("should_store", False):

                                save_memory(
                                    summary,
                                    analysis.get("category", "general"),
                                    analysis.get("importance", 5)
                                )

                                print("[MEMORY SAVED]")

            except Exception as memory_error:

                print(f"[MEMORY ERROR] {memory_error}")

            # ==========================
            # LOAD MEMORIES
            # ==========================

            print("[ASKING LLM]")

            relevant = get_relevant_memories(user_text)

            if relevant:

                memories = "\n".join(
                    f"- {mem[1]}"
                    for mem in relevant[:10]
                )

            else:

                memories = "No relevant memories."
            print(f"[MEMORY CHARS] {len(memories)}")
            

# ==========================
# SAVE USER MESSAGE
# ==========================

            save_chat_message(
                "user",
                user_text
            )

            # ==========================
            # LOAD TODAY CHAT
            # ==========================

            recent_chat = get_recent_chat(2)

            # ==========================
            # BUILD PROMPT
            # ==========================

            prompt = f"""
            {SYSTEM_PROMPT}

            LONG TERM MEMORIES:

            {memories}

            TODAY'S CONVERSATION:

            {recent_chat}

            CURRENT USER EMOTION:

            Emotion: {emotion_data['emotion']}
            Sentiment: {emotion_data['sentiment']}
            Intensity: {emotion_data['intensity']}

            Use this emotional context when responding.
            Be emotionally aware and supportive when appropriate.

            USER:
            {user_text}

            KRITI:
            """

            # ==========================
            # MAIN LLM CALL
            # ==========================

            t4 = time.time()

            print(f"[PROMPT LENGTH] {len(prompt)}")

            reply = ask_llm(prompt)

            print(
                f"[MAIN LLM TIME] "
                f"{time.time() - t4:.2f} sec"
            )

            print("[LLM FINISHED]")

            save_chat_message(
                "assistant",
                reply
            )
        except Exception as e:

            print(f"[ERROR] {e}")

            reply = (
                "Oops! A tiny prehistoric bird "
                "stole my thoughts for a moment. 🐦"
            )

        safe_reply = (
            reply.replace("\\", "\\\\")
                 .replace("'", "\\'")
                 .replace("\n", "\\n")
        )

        self.window.evaluate_js(
            f"addKritiMessage('{safe_reply}')"
        )

        threading.Thread(
            target=speak,
            args=(reply,),
            daemon=True
        ).start()

        self.window.evaluate_js(
            "setStatus('Online')"
        )

# ==========================================
# MAIN
# ==========================================

def main():
    init_db()
    html_file = os.path.join(
        PROJECT_ROOT,
        "index.html"
    )

    if not os.path.exists(html_file):

        print(
            f"Error: Could not find index.html at\n{html_file}"
        )

        sys.exit(1)

    print("=" * 50)
    print("🌿 Launching Kriti Desktop AI Assistant...")
    print("=" * 50)
    
    window = webview.create_window(
        title="Kriti - Creative AI Companion",
        url=f"file:///{html_file.replace(os.sep, '/')}",
        width=1150,
        height=820,
        min_size=(780, 580),
        frameless=False,
        easy_drag=True,
        background_color="#05120c"
    )

    api = KritiPythonAPI(window)

    window.expose(
        api.on_user_message
    )

    webview.start(
        debug=False
    )

# ==========================================
# START
# ==========================================

if __name__ == "__main__":
    main()