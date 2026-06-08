#Multiple input graph 

from typing import List, Dict, TypedDict
from langgraph.graph import StateGraph 

class AgentState (TypedDict):
    values : List[int]
    name : str
    result : str

def process_values (state: AgentState) -> AgentState:
    """This Function handles different multiple inputs and process them to generate a result"""

    state["result"] = f"Hello {state['name']} ! The sum of your values {state['values']} is {sum(state['values'])}"

    return state

graph = StateGraph (AgentState)
graph.add_node("processor", process_values)  
graph.set_entry_point("processor")
graph.set_finish_point("processor")
app = graph.compile()

result = app.invoke({"values":[1,2,3,4], "name":"Vishesh"})

print(result["result"])
