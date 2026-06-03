from langchain_community.document_loaders import PyPDFLoader

data = PyPDFLoader("RAG project/GRU.pdf")

docs = data.load()

print (docs[2])

