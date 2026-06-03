from langchain_community.document_loaders import TextLoader

data = TextLoader("RAG project/notes.txt")

docs = data.load()

print (docs)