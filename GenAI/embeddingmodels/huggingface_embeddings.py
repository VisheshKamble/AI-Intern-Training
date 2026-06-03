from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"

)
texts = [
    "Hello this is Vishesh",
    "Hello your name is YouTube",
    "And you all are very beautiful"
]



vector = embedding.embed_documents(texts)

print(vector)