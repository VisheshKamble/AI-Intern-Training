#Create a ChatBot with memory for our agent 
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List , Dict , Union

load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")

