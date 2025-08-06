from db import ticket
from chatbot.myprompt import (
    solution_prompt,
    similarity_check_prompt,
    severity_prompt,
    category_prompt,
)
from langchain_ollama import OllamaLLM
from langchain_core.runnables import RunnableSequence

llm = OllamaLLM(model="gemma3")  # e.g., "llama3", "mistral"

solution_chain: RunnableSequence = solution_prompt | llm
similarity_check_chain: RunnableSequence = similarity_check_prompt | llm
severity_check_chain: RunnableSequence = severity_prompt | llm
category_chain: RunnableSequence = category_prompt | llm


def get_complain_solution(user_complain: str) -> str:
    return solution_chain.invoke({"user_complain": user_complain})


def get_severity_level(user_complain: str) -> str:
    return severity_check_chain.invoke({"user_complain": user_complain}).strip().title()


def get_category(user_complain: str) -> str:
    return category_chain.invoke({"user_complain": user_complain}).strip()


def get_similar_solution(user_complain: str) -> str:
    c2 = user_complain
    resolved_tickets = ticket.get_resolved_tickets()
    for t in resolved_tickets:
        c1 = t.main_description + "\n" + t.other_description
        are_complains_similar = similarity_check_chain.invoke(
            {"complaint_1": c1, "complaint_2": c2}
        )
        if are_complains_similar == "true":
            return t.remark
    return None


if __name__ == "__main__":
    user_complain = (
        "Unable to do an UPI Transaction while Purchasing Laptop from Amazon"
    )
    user_complain = "Poor Product Quality"
    user_complain = "My Wifi Router is not Working"
    print(f"User Complain: {user_complain}")
    res = get_severity_level(user_complain)
    print(f"Res: \n{res}")
