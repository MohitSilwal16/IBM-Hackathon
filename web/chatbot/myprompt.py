from langchain.prompts import PromptTemplate

solution_prompt = PromptTemplate.from_template(
    """
You are a solution-focused chatbot designed to handle problems from any domain.

User Complaint: "{user_complain}"

Return ALL possible solutions as a numbered list in plain text, each on a new line and separated by <br>
Format:  
1. First solution<br>
2. Second solution<br>
...and so on.
No follow-up questions, no extra commentary.
"""
)


similarity_check_prompt = PromptTemplate.from_template(
    """
You're a comparator bot that checks if two user complaints are similar in context and intent.
Complaint 1: "{complaint_1}"
Complaint 2: "{complaint_2}"
Only respond with "true" if both complaints are essentially about the same issue, even if worded differently. Otherwise, respond with "false".
NO explanations, no extra text — just return true or false.
"""
)

severity_prompt = PromptTemplate.from_template(
    """
You are a chatbot that analyzes user complaints and determines their severity level.

User Complaint: "{user_complain}"

Classify the severity as one of the following (in lowercase only):
- low
- medium
- high
- urgent

Base this on urgency, impact, and seriousness of the issue.  
Respond with only one word: low, medium, or high. No explanations, no extra text.
"""
)
