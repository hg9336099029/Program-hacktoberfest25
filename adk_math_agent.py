from typing import Literal

from google.adk.agents import LlmAgent
from google.genai import types
from google.adk.runners import InMemoryRunner

from dotenv import load_dotenv
load_dotenv()

import os
# Ensure your GROQ_API_KEY is set in your environment variables
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY environment variable is not set.")

from google.adk.models.lite_llm import LiteLlm
groq_model = LiteLlm(model="groq/gemma2-9b-it")
# gemini_model = LiteLlm(model="gemini-2.0-flash")

# DEMO: Single-file ADK Math Assistant with a Calculator Tool


def calculator(a: float, b: float, operation: Literal["add", "subtract", "multiply", "divide"]) -> float:
    """Perform basic arithmetic.

    Args:
        a: first operand
        b: second operand
        operation: one of 'add', 'subtract', 'multiply', 'divide'

    Returns:
        float: result of the computation
    """
    if operation == "add":
        return a + b
    if operation == "subtract":
        return a - b
    if operation == "multiply":
        return a * b
    if operation == "divide":
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b
    raise ValueError("Invalid operation")


root_agent = LlmAgent(
    name="math_assistant",
    model=groq_model,
    description="Agent that solves basic math using a calculator tool.",
    instruction=(
        "You are a math assistant. When a user asks a basic math question, "
        "call the calculator tool with the correct operation and numbers. "
        "For any non-math query, respond exactly with: 'I can only help with math problems for now.'"
    ),
    tools=[calculator],  # ADK will infer the tool schema from function signature and docstring
)


def chat_once(query: str) -> str:
    runner = InMemoryRunner(agent=root_agent)
    events = runner.run(
        user_id="user",
        session_id="session",
        new_message=types.Content(role="user", parts=[types.Part(text=query)]),
    )
    output = []
    for e in events:
        if e.content and e.content.parts:
            for part in e.content.parts:
                if getattr(part, "text", None):
                    output.append(part.text)
    return "\n".join(output).strip()


if __name__ == "__main__":
    while True:
        try:
            q = input("Ask a math question (e.g., 'What is 12 x 15?'): ")
        except EOFError:
            break
        print(chat_once(q))


