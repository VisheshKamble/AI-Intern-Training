from typing import List, Dict, TypedDict
from langgraph.graph import StateGraph 

class AgentState (TypedDict):
    message: str

    def greeting_node (state: AgentState) -> AgentState:
        """Simple node that add a greeting to the state message"""
        state["message"] = "Hello! " + state["message"] + " , How is your day?" 
        return state
    
graph = StateGraph (AgentState)
graph.add_node("greeting", AgentState.greeting_node)

graph.set_entry_point("greeting")
graph.set_finish_point("greeting")

app = graph.compile()

result = app.invoke({"message": "Vishesh"})

print(result["message"])