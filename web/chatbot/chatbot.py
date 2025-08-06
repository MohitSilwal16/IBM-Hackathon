from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from langchain_core.runnables import RunnableSequence

llm = OllamaLLM(model="gemma3")  # e.g., "llama3", "mistral"
solution_prompt = PromptTemplate.from_template(
    """
You're a problem-solving chatbot specialized in the E-Commerce domain.
User Complaint: "{user_complain}"
If the complaint is NOT related to E-Commerce (e.g., product issues, payments, delivery, returns, account, cart, offers, orders, etc.), reply: "Sorry, I can only help with E-Commerce related problems."
If it IS related, assume the problem occurred on the user's respective E-Commerce website. List ALL possible solutions in plain text only. No markdown, no follow-up questions, no extra commentary. Be clear, concise, and exhaustive.
"""
)

solution_chain: RunnableSequence = solution_prompt | llm


def get_complain_solution(user_complain: str) -> str:
    return solution_chain.invoke({"user_complain": user_complain})


if __name__ == "__main__":
    user_complain = "My Wifi Router is not Working"
    user_complain = "Unable to do an UPI Transaction while Purchasing Laptop from Amazon"
    res = get_complain_solution(user_complain)
    print(f"Res: \n{res}")
