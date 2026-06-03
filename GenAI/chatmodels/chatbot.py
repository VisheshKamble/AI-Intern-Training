from dotenv import load_dotenv

from langchain_groq import ChatGroq #Groq

load_dotenv()  

model = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct") #Groq

print ("Welcome enter 0 to exit")

while True:

    prompt = input("Ask me anything : ")

    if prompt == "0":
        print("Goodbye!")
        break

    response = model.invoke(prompt)

    print("Bot : ", response.content)