from dotenv import load_dotenv
from langchain_groq import ChatGroq #Groq
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

data = TextLoader("RAG project/notes.txt")

docs = data.load()

template = ChatPromptTemplate.from_messages([
    ('system',"""You are a helpful assistant for question answering. """),
    ('user', "{data}")
])

model = ChatGroq(model = 'meta-llama/llama-4-scout-17b-16e-instruct')

prompt = template.invoke({"data": docs[0].page_content})

response = model.invoke(prompt)

print(response.content)
