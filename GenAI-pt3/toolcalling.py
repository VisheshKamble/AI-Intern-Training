from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import tool
from rich import print

#creating a tool using decorator

@tool
def get_text_length(text : str) -> int:
    """" Return the number of characters in the input text"""
    return len(text)

llm = ChatGroq(model = "meta-llama/llama-4-scout-17b-16e-instruct")

#tool binding 
llm_with_bind = llm.bind_tools([get_text_length])