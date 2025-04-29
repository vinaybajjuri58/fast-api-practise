from fastapi import FastAPI
from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from groq import Groq
from pydantic import BaseModel
import uvicorn
load_dotenv()

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
vectorstore = QdrantVectorStore(
    client=client,
    collection_name="taxation",
    embedding=embeddings
)

class ChatInput(BaseModel):
    text: str

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/chat")
def chat_endpoint(input: ChatInput):
    return {"reply": f"You said: {input.text}"}





