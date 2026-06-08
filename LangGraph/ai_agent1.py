#main goal is to integrate LLMs into a Graph
from typing import TypedDict, List
from langgraph.graph import StateGraph , START , END
from groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

