# from db import ticket
from chatbot.myprompt import solution_prompt, similarity_check_prompt, severity_prompt
from langchain_ollama import OllamaLLM
from langchain_core.runnables import RunnableSequence

llm = OllamaLLM(model="gemma3")  # e.g., "llama3", "mistral"

solution_chain: RunnableSequence = solution_prompt | llm
similarity_check_chain: RunnableSequence = similarity_check_prompt | llm
severity_check_chain: RunnableSequence = severity_prompt | llm


def get_complain_solution(user_complain: str) -> str:
    return solution_chain.invoke({"user_complain": user_complain})


def get_severity_level(user_complain: str) -> str:
    return severity_check_chain.invoke({"user_complain": user_complain})


# def get_similar_solution(user_complain: str) -> ticket.Ticket:
#     resolved_tickets = ticket.get_resolved_tickets()
#     for t in resolved_tickets:
#         if t.main_description == user_complain:
#             return t
#     return None


if __name__ == "__main__":
    user_complain = (
        "Unable to do an UPI Transaction while Purchasing Laptop from Amazon"
    )
    user_complain = "Poor Product Quality"
    user_complain = "My Wifi Router is not Working"
    print(f"User Complain: {user_complain}")
    res = get_severity_level(user_complain)
    print(f"Res: \n{res}")
