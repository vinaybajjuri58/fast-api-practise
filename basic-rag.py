from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv
from groq import Groq

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

docs = vectorstore.similarity_search("What is the tax on income?", k=10 )
context_text = "\n\n".join([doc.page_content for doc in docs])

messages = [
        {
            "role": "system",
            "content": """f"You are expert in indian taxation. Assist the user with their queries on how to optimise their tax regime 
            ,deductions and exceptions so that they can save more on their taxes. Feel free to ask questions for more details from 
             the user to give him a better answer
              Use the following context to answer user questions:\n\n{context_text}" """
        },
        {
            "role": "user",
            "content": "Which is the best tax regime and deductions available for a salaried individual with an annual income of 10 lakhs?"
        }
    ]

chat_completion = groq_client.chat.completions.create(
    messages=messages,
        model="gemma2-9b-it",
    )


response = chat_completion.choices[0].message.content

print(response)


















