#looping agent example using LangGraph
from typing import TypedDict, List
import random
from langgraph.graph import StateGraph, START, END

# 1. Define the State
class AgentState(TypedDict):
    name: str
    number: List[int]
    counter: int 

# 2. Define the Nodes
def greeting_node(state: AgentState) -> AgentState:
    """Greeting node that says hello to the user"""
    # Fixed: Mixed single quotes inside the double-quoted f-string
    state["name"] = f"Hello {state['name']} !"
    state["counter"] = 0
    return state

def random_node(state: AgentState) -> AgentState:
    """Generates a random number from 0 to 10 and increments counter"""
    state["number"].append(random.randint(0, 10))
    state["counter"] += 1
    return state

# 3. Define the Conditional Routing Function
# Note: It takes state, but returns a string path!
def should_continue(state: AgentState) -> str:
    """Function to decide whether to loop or exit"""
    if state["counter"] < 5:
        print("Entering Loop, Current Counter:", state["counter"])
        return "loop"
    else:
        print("Max iterations reached. Exiting.")
        return "exit"
    
# 4. Build the Graph
graph = StateGraph(AgentState)

graph.add_node("greeting", greeting_node)
graph.add_node("random", random_node)

# Set the entry point using the modern START edge
graph.add_edge(START, "greeting")
graph.add_edge("greeting", "random")

# Add conditional edge looping back to "random" or ending at END
graph.add_conditional_edges(
   "random",
   should_continue,
   {
    "loop": "random",       # Maps the string "loop" back to the "random" node
    "exit": END            # Maps the string "exit" to the END node
   }
)

# 5. Compile and Invoke
app = graph.compile()

# Starting state
result = app.invoke({"name": "Vishesh", "number": [], "counter": 0})

print("\n--- Final Result ---")
print("Greeting:", result["name"])
print("Numbers Generated:", result["number"])
print("Final Counter:", result["counter"])