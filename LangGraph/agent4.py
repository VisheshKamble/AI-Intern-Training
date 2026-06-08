#Conditional Graph Agent
from typing import TypedDict
from langgraph.graph import StateGraph , START , END

class AgentState (TypedDict):
    number1 : int
    operation : str
    number2 : int
    finalnumber : int

def adder (state: AgentState) -> AgentState:
    """This node adds the two numbers in the state and stores the result in finalnumber"""

    state["finalnumber"] = state["number1"] + state["number2"]

    return state

def subtractor (state: AgentState) -> AgentState:
    """This node subtracts the two numbers in the state and stores the result in finalnumber"""

    state["finalnumber"] = state["number1"] - state["number2"]

    return state

def decide_next_node (state: AgentState) -> AgentState:
    """This node decides the next node to execute based on the operation in the state"""

    if state["operation"] == "+":
        return "addition"
    elif state["operation"] == "-":
        return "subtraction"
    

graph = StateGraph (AgentState)
graph.add_node("add_node" , adder)
graph.add_node("subtract_node" , subtractor)
graph.add_node("router" , lambda state : state)
graph.add_edge(START, "router")

graph.add_conditional_edges(
    "router",
    decide_next_node,
    {
        "addition": "add_node",
        "subtraction": "subtract_node"
    }
)

graph.add_edge("add_node", END)
graph.add_edge("subtract_node", END)

app = graph.compile()

result = app.invoke({"number1": 10, "operation": "+", "number2": 5})

print(result["finalnumber"])

