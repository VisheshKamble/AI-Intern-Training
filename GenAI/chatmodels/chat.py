from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

#from langchain.chat_models import init_chat_model #ChatGPT
from langchain_google_genai import ChatGoogleGenerativeAI #Gemini

from langchain.chat_models import init_chat_model

#model = ChatGoogleGenerativeAI(model="gemini-2.0-flash") #Gemini

#response = model.invoke("give me a paragraph on GEN-AI ?")

#print(response.content)


model = init_chat_model("groq:meta-llama/llama-4-scout-17b-16e-instruct") #ChatGPT

response = model.invoke("give me a paragraph on GEN-AI ?")

print(response.content)