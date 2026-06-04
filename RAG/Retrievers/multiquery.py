from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_groq import ChatGroq 
from dotenv import load_dotenv

load_dotenv()

docs = [
    Document(page_content="Gradient descent is an optimization algorithm used in machine learning."),
    Document(page_content="Gradient descent minimizes the loss function."),
    Document(page_content="Gradient descent is an optimization that minimizes the loss function."),
    Document(page_content="Neural networks use gradient descent for training."),
    Document(page_content="Support Vector Machines are supervised learning algorithms.")
]

# Using the modern HuggingFace package
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = Chroma.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever()

# Initialize Groq LLM
# Common models: "llama-3.1-70b-versatile" or "mixtral-8x7b-32768"
llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0
)

multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=retriever,
    llm=llm
)

query = "What is gradient descent?"
retrieved_docs = multi_query_retriever.invoke(query)

print("\nRetrieved Documents:\n")
for doc in retrieved_docs:
    print(f"- {doc.page_content}")