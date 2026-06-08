#Sequential Graph
#create and handle multiple nodes in a LangGraph agent

from typing import TypedDict
from langgraph.graph import StateGraph 

class AgentState (TypedDict):
    name : str
    age : int
    final : str

#first node of our sequence

def first_node (state: AgentState) -> AgentState:
    """This is the first node of our sequence"""

    state['final'] = f"Hello {state['name']}!"

    return state  

#second node of our sequence

def second_node (state: AgentState) -> AgentState:
    """This is the second node of our sequence"""

    state['final'] += f" You are {state['age']} years old."

    return state

graph = StateGraph (AgentState)
graph.add_node("first" , first_node)
graph.add_node("second" , second_node)
graph.set_entry_point("first")
graph.add_edge("first", "second")
graph.set_finish_point("second")

app = graph.compile()

result = app.invoke({"name":"Vishesh", "age": 22})

print(result["final"])