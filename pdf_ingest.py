from langchain.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from database import get_connection

embeddings = OpenAIEmbeddings()

def ingest_pdf(path):

    loader = PyPDFLoader(path)

    pages = loader.load()

    conn = get_connection()
    cur = conn.cursor()

    for page in pages:

        text = page.page_content

        vector = embeddings.embed_query(text)

        cur.execute(
            "INSERT INTO knowledge (content, embedding) VALUES (%s,%s)",
            (text, vector)
        )

    conn.commit()

    cur.close()
    conn.close()
