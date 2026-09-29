import time
import ollama

MODEL = "qwen2.5:7b"

def ask_llm(prompt):

    print(f"[PROMPT CHARS] {len(prompt)}")

    start = time.time()

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    elapsed = time.time() - start

    answer = response["message"]["content"]

    print(f"[ANSWER CHARS] {len(answer)}")
    print(f"[LLM TIME] {elapsed:.2f} sec")

    if elapsed > 0:
        print(
            f"[TOKENS EST] "
            f"{len(answer)/4:.0f}"
        )
        print(
            f"[CHARS/SEC] "
            f"{len(answer)/elapsed:.2f}"
        )

    return answer