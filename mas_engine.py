from knowledge import search_knowledge
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

def ask_ai(question):

    docs = search_knowledge(question)

    if docs:
        prompt = f"""
Use the following knowledge to answer the question.

Knowledge:
{docs}

Question:
{question}
"""
    else:
        prompt = question

    response = llm.invoke(prompt)

    return response.content
