import requests
from bs4 import BeautifulSoup
from database import get_connection
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

def ingest_url(url):

    response = requests.get(url)

    soup = BeautifulSoup(response.text,"html.parser")

    text = soup.get_text()

    vector = embeddings.embed_query(text)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO knowledge (content, embedding) VALUES (%s,%s)",
        (text, vector)
    )

    conn.commit()

    cur.close()
    conn.close()
