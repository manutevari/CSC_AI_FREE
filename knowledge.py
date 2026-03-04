from database import get_connection
from langchain_community.embeddings import HuggingFaceEmbeddings
import numpy as np

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def dynamic_top_k(question):

    length = len(question.split())

    if length < 5:
        return 2
    elif length < 12:
        return 4
    else:
        return 6


def search_knowledge(question):

    query_embedding = embeddings.embed_query(question)

    top_k = dynamic_top_k(question)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT content, embedding FROM knowledge")

    rows = cur.fetchall()

    scores = []

    for content, vector in rows:

        vector = np.array(vector)

        score = np.dot(query_embedding, vector)

        scores.append((score, content))

    scores.sort(reverse=True)

    results = [r[1] for r in scores[:top_k]]

    cur.close()
    conn.close()

    if results:
        return "\n".join(results)

    return None
