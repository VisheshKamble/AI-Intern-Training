from dotenv import load_dotenv
from langchain_groq import ChatGroq #Groq
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

#data = TextLoader("RAG project/notes.txt") #loading the text file

#docs = data.load()

data = PyPDFLoader("RAG project/deeplearning.pdf") #Loading the PDF file 

docs = data.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000, 
    chunk_overlap = 200
)

chunks = splitter.split_documents(docs)

template = ChatPromptTemplate.from_messages([
    ('system',"""You are a helpful assistant for question answering. """),
    ('user', "{data}")
])

model = ChatGroq(model = 'meta-llama/llama-4-scout-17b-16e-instruct')

prompt = template.invoke({"data": docs[0].page_content})

response = model.invoke(prompt)

print(response.content)
