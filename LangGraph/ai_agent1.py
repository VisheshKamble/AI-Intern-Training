#main goal is to integrate LLMs into a Graph
from typing import TypedDict, List
from langgraph.graph import StateGraph , START , END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

class AgentState (TypedDict):
    message : List[HumanMessage]

llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")

def process(state : AgentState) -> AgentState:
    #processing the message and generating a response
    response = llm.invoke(state["message"])
    print(f"AI : {response.content}")
    return state

#defining the graph
graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()

user_input = input("You: ")
while user_input.lower() != "exit":
    state = {"message": [HumanMessage(content=user_input)]}
    agent.invoke(state)
    user_input = input("You: ")