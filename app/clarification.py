import re
from app.llm import ask_llm


def analyze_question(question: str) -> dict:
    """
    Determine whether a database question needs clarification.
    """

    prompt = f"""
You are an AI assistant that analyzes database questions.

Determine whether the user's question is ambiguous enough
that generating SQL immediately could produce an incorrect result.

USER QUESTION:
{question}

Rules:

- If the question is clear, respond with exactly:
NO

- If important information is missing, respond with exactly:
YES
CLARIFICATION: <one concise follow-up question>

Examples:

Question:
Show me customers from Delhi.

Answer:
NO

Question:
Show me the top customers.

Answer:
YES
CLARIFICATION: How should customers be ranked — by total spending or number of orders?

Question:
Show me orders above 3000.

Answer:
NO

Do not generate SQL.
Do not explain your reasoning.

Now analyze the question:
{question}
"""

    response = ask_llm(prompt).strip()

    # Normalize the response
    response_upper = response.upper()

    # Check whether clarification is needed
    if response_upper.startswith("YES"):

        clarification = None

        # Look for "CLARIFICATION:"
        match = re.search(
            r"CLARIFICATION\s*:\s*(.+)",
            response,
            re.IGNORECASE | re.DOTALL
        )

        if match:
            clarification = match.group(1).strip()

        # Fallback if the model says YES but doesn't provide
        # the expected label
        if not clarification:
            clarification = (
                "Could you provide more details about what you mean?"
            )

        return {
            "needs_clarification": True,
            "clarification": clarification
        }

    return {
        "needs_clarification": False,
        "clarification": None
    }


if __name__ == "__main__":

    question = "Show me the top customers."

    result = analyze_question(question)

    print(result)