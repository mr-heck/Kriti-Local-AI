print("GUI.PY LOADED")
import tkinter as tk
from tkinter import scrolledtext

from ollama import chat

from Database.memory import *
from Database.tasks import *
from Database.task_extractor import extract_task
from Database.memory_detector import detect_memory
from Database.memory_extractor import extract_memory
from Database.memory_analyzer import analyze_memory
from Nova.personality import load_personality
from listen import listen
from voice import speak


init_db()
init_tasks_db()
personality = load_personality()

conversation_history = []

OWNER_KEY = "ALPHANOVA2026"


def start_nova():
    window = tk.Tk()
    window.title(personality["name"])
    window.geometry("900x650")

    chat_box = scrolledtext.ScrolledText(
        window,
        wrap=tk.WORD,
        width=100,
        height=30,
    )
    chat_box.pack(padx=10, pady=10)
    chat_box.insert(
        tk.END,
        f"{personality['name']}: Creative systems ready.\n\n",
    )

    user_input = tk.Entry(window, width=80)
    user_input.pack(side=tk.LEFT, padx=10, pady=10)

    def listen_message():
        heard_text = listen()

        if heard_text:
            user_input.delete(0, tk.END)
            user_input.insert(0, heard_text)
            send_message()

    def send_message():
        global conversation_history

        message = user_input.get().strip()
        print("DEBUG TEST")
        if not message:
            return

                # Automatic memory pipeline

        print(f"[USER] {message}")

        has_memory = detect_memory(message)

        print(f"[DETECTOR] {has_memory}")

        if has_memory:

            summary = extract_memory(message)

            print(f"[SUMMARY] {summary}")

            if summary:

                analysis = analyze_memory(summary)

                print(f"[ANALYSIS] {analysis}")

                if analysis["should_store"] or analysis["importance"] >= 5:

                    save_memory(
                        summary=summary,
                        category=analysis["category"],
                        importance=analysis["importance"]
                    )

                    print("[MEMORY SAVED]")


        task = extract_task(message)

        if task:
            add_task(task)
            print(f"[TASK ADDED] {task}")

        if message.lower().startswith("add task "):
            task_text = message[9:].strip()
            add_task(task_text)
            chat_box.insert(
                tk.END,
                f"{personality['name']}: Task added.\n\n",
            )
            chat_box.see(tk.END)
            return

        chat_box.insert(tk.END, f"You: {message}\n")
        user_input.delete(0, tk.END)

        if message.lower().startswith("remember that "):
            memory_value = message[len("remember that "):].strip()

            save_memory(
                summary=memory_value,
                category="manual",
                importance=10,
            )

            chat_box.insert(
                tk.END,
                f"{personality['name']}: I'll remember that.\n\n",
            )

            chat_box.see(tk.END)
            return

        if message.lower() == "show memories":
            memories = show_all()

            if not memories:
                chat_box.insert(
                    tk.END,
                    f"{personality['name']}: No memories stored.\n\n",
                )
            else:
                chat_box.insert(tk.END, f"{personality['name']}:\n")

                for mem_id, summary, category, importance, created_at in memories:
                    chat_box.insert(
                    tk.END,
                    f"{mem_id}. [{importance}] [{category}] {summary}\n",
                )
                chat_box.insert(tk.END, "\n")

            chat_box.see(tk.END)
            return

        if message.lower() == "show tasks":
            tasks = show_tasks()

            if not tasks:
                chat_box.insert(
                    tk.END,
                    f"{personality['name']}: No tasks found.\n\n",
                )
            else:
                chat_box.insert(tk.END, f"{personality['name']} Tasks:\n")

                for task_id, task, status, priority in tasks:
                    chat_box.insert(
                        tk.END,
                        f"{task_id}. [{priority}] {task} ({status})\n",
                    )

                chat_box.insert(tk.END, "\n")

            chat_box.see(tk.END)
            return

        if message.lower().startswith("complete task "):
            try:
                task_id = int(message.replace("complete task ", ""))
                complete_task(task_id)
                chat_box.insert(
                    tk.END,
                    f"{personality['name']}: Task completed.\n\n",
                )
            except ValueError:
                chat_box.insert(
                    tk.END,
                    f"{personality['name']}: Invalid task ID.\n\n",
                )

            chat_box.see(tk.END)
            return

        if message.lower().startswith("delete task "):
            try:
                task_id = int(message.replace("delete task ", ""))
                delete_task(task_id)
                chat_box.insert(
                    tk.END,
                    f"{personality['name']}: Task deleted.\n\n",
                )
            except ValueError:
                chat_box.insert(
                    tk.END,
                    f"{personality['name']}: Invalid task ID.\n\n",
                )

            chat_box.see(tk.END)
            return

        if message.lower() == "backup memories":
            backup_file = backup_memory()
            chat_box.insert(
                tk.END,
                f"{personality['name']}: Backup created.\n"
                f"{backup_file}\n\n",
            )
            chat_box.see(tk.END)
            return

        if message.lower().startswith("delete memory "):
            try:
                memory_id = int(message.replace("delete memory ", ""))
                delete_memory(memory_id)
                chat_box.insert(
                    tk.END,
                    f"{personality['name']}: Memory {memory_id} deleted.\n\n",
                )
            except ValueError:
                chat_box.insert(
                    tk.END,
                    f"{personality['name']}: Invalid memory ID.\n\n",
                )

            chat_box.see(tk.END)
            return

        if message.startswith("nova wipe memory "):
            key = message.replace("nova wipe memory ", "").strip()

            if key == OWNER_KEY:
                backup_file = backup_memory()
                wipe_all_memories()
                chat_box.insert(
                    tk.END,
                    f"{personality['name']}: Memory wiped.\n"
                    f"Backup saved:\n{backup_file}\n\n",
                )
            else:
                chat_box.insert(
                    tk.END,
                    f"{personality['name']}: Access denied.\n\n",
                )

            chat_box.see(tk.END)
            return

        all_memories = show_all()
        memory_text = ""

        for _, summary, category, importance, _ in all_memories:
            memory_text += (
                f"[{importance}] [{category}] {summary}\n"
            )

        if memory_text == "":
            memory_text = "No memories stored."
        
        from time_utils import (
            get_current_time,
            get_current_date,
            get_day
        )

        system_prompt = f"""
You are {personality['name']}.

Current Time:
{get_current_time()}

Current Date:
{get_current_date()}

Current Day:
{get_day()}

Creator:
{personality['creator']}

Role:
{personality['role']}

Traits:
{', '.join(personality['traits'])}

Description:
{personality['description']}

Rules:

Important Rules:

- You have access to the user's stored memories.
- When the user asks about themselves, use the memories provided.
- When asked "Who am I?", answer using stored memories.
- When asked "What is my dream?", answer using stored memories.
- Do not say you don't know the user if relevant memories exist.
- Memories are factual unless corrected by the creator.

Memories:

{memory_text}
"""

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]
        messages.extend(conversation_history)
        messages.append(
            {
                "role": "user",
                "content": message,
            }
        )

        try:
            response = chat(
                model="qwen2.5:7b",
                messages=messages,
                options={"temperature": 0.8},
            )
            reply = response["message"]["content"]

            try:
                speak(reply)
            except Exception as error:
                print(f"Voice error: {error}")
        except Exception as error:
            reply = f"Error: {error}"

        conversation_history.append(
            {
                "role": "user",
                "content": message,
            }
        )
        conversation_history.append(
            {
                "role": "assistant",
                "content": reply,
            }
        )

        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]

        chat_box.insert(
            tk.END,
            f"{personality['name']}: {reply}\n\n",
        )
        chat_box.see(tk.END)

    send_button = tk.Button(
        window,
        text="Send",
        command=send_message,
    )
    mic_button = tk.Button(
        window,
        text="🎤",
        command=listen_message,
    )

    mic_button.pack(side=tk.LEFT, padx=5)
    send_button.pack(side=tk.LEFT, padx=5)

    user_input.bind(
        "<Return>",
        lambda event: send_message(),
    )

    window.mainloop()
