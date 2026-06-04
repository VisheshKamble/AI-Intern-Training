from dotenv import load_dotenv
from langchain_groq import ChatGroq #Groq
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

model = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")

embedding_models = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = Chroma(
    persist_directory="chroma-db",
    embedding_function=embedding_models
)

retriever = vectorstore.as_retriever(
    search_type = "mmr",
    search_kwargs = {"k": 4, "fetch_k": 10 , "lambda_mult": 0.5}
)

llm = ChatGroq( model = "meta-llama/llama-4-scout-17b-16e-instruct")

#prompt template 

prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         """You are a helpful AI assistant.
         
         Use Only the provided context to answer the question.
         
         If the answer is not present in the context ,
         say that answer is not available in the document."""),
        ("human", """Context: {context}
         
         Question: {question}""")
    ]
)

print ("Welcome to RAG System! Enter 0 to exit")

while True:
    query = input("You : ")
    if query == "0":
        break
    docs = retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in docs])

    final_prompt = prompt.invoke(
        {
            "context": context,
            "question": query
        }
    )

    response = llm.invoke(final_prompt)

    print("Bot : ", response.content)