from dotenv import load_dotenv

from langchain_groq import ChatGroq #Groq

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()  

model = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct") #Groq

print ("Welcome enter 0 to exit")

messages = [
    SystemMessage(content="You are a research assistant."),
]

while True:

    prompt = input("Ask me anything : ")



    if prompt == "0":
        print("Goodbye!")
        break

    messages.append(HumanMessage(content=prompt))

    response = model.invoke(messages)
    
    messages.append(AIMessage(content=response.content))    

    print("Bot : ", response.content)
