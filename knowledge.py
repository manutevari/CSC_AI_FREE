from database import get_connection
from langchain_openai import OpenAIEmbeddings
import numpy as np

embeddings = OpenAIEmbeddings()

def search_knowledge(question, top_k=3):

    query_embedding = embeddings.embed_query(question)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT content, embedding FROM knowledge"
    )

    rows = cur.fetchall()

    scores = []

    for r in rows:
        content = r[0]
        vector = r[1]

        score = np.dot(query_embedding, vector)

        scores.append((score, content))

    scores.sort(reverse=True)

    results = [s[1] for s in scores[:top_k]]

    cur.close()
    conn.close()

    if results:
        return "\n".join(results)

    return None
