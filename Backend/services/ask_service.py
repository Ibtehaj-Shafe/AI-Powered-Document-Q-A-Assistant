import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from Backend.models.document import Document
from groq import Groq
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from Backend.models import UserStats,Document

# Load environment variables
load_dotenv()
key = os.getenv("db_key")          # Pinecone API key
index_name = os.getenv("index_name")
g_key = os.getenv("api_key")       # Groq API key

# Initialize Pinecone client
pc = Pinecone(api_key=key)
index = pc.Index(index_name)

# Initialize Groq client
groq_client = Groq(api_key=g_key)

# Initialize SentenceTransformer for embeddings
embedder = SentenceTransformer("all-MiniLM-L6-v2")


def process_query(query: str, user_id: int, db: Session) -> str:
    """
    Handles the full query workflow:
    1. Embed the query with SentenceTransformer
    2. Search Pinecone for top matches
    3. Build context from retrieved chunks
    4. Ask Groq LLM with context + query
    5. Increment user's question count in DB
    """
    doc_user = db.query(Document).filter(Document.user_id == user_id).all()
    if not doc_user:
        return "No documents found for this user. Please upload documents first."
    # 1. Embed query locally
    query_embedding = embedder.encode(query).tolist()

    # 2. Search Pinecone
    results = index.query(
        vector=query_embedding,
        top_k=5,
        include_metadata=True,              # Include metadata in the results like chunk text, filename etc
        filter={"user_id": user_id}         # Ensures only this user’s documents are searched.
    )

    # 3. Build context from retrieved chunks
    context = ""
    for match in results["matches"]:            #  results["matches"] list of the top‑k chunks that matched the query
        chunk_text = match["metadata"]["chunk"]
        context += chunk_text + "\n"


    # 4. Ask Groq LLM
    prompt = (
    f"Answer the following question based on the provided context.\n\n"
    f"Context:\n{context}\n\n"
    f"Question: {query}\n\n"
    f"If the context does not contain relevant information, "
    f"clearly state: 'I am unable to find data related to the query.'"
   ) 

    chat_response = groq_client.chat.completions.create(                #  chat.completions.create -> return multiple possible completions.
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    """
    .message contains dict like
    {
    "role": "assistant",
    "content": "AI stands for Artificial Intelligence..."
    }

    """

    answer = chat_response.choices[0].message.content

    # 5. Increment question count in DB Class name: UserStats
    stats = db.query(UserStats).filter(UserStats.user_id == user_id).first()
    if not stats:
        stats = UserStats(user_id=user_id, questions_asked_count=1)
        db.add(stats)
    else:
        stats.questions_asked_count += 1
    db.commit()

    return answer
