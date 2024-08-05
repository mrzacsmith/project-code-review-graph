import os
from typing import List, Dict
from langchain.llms import OpenAI
from langgraph.graph import StateGraph, Graph
from typing import List, Dict, TypedDict

# Define the state structure
class State(TypedDict):
    current_file: str
    reviewed_files: List[str]
    reviews: Dict[str, str]

# Initialize LLM
llm = OpenAI()

# Define graph
workflow = StateGraph(State)

# Define nodes 
def traverse_files(state):
    pass

def review_code(state):
    pass

def generate_markdown(state):
    pass

# Add nodes to graph
workflow.add_node("traverse", traverse_files)
workflow.add_node("review", review_code)
workflow.add_node("generate", generate_markdown)

# Define edges 
workflow.add_edge("traverse", "review")
workflow.add_edge("review", "generate")

# Set entry point
workflow.set_entry_point("traverse")

# Compile the graph
graph = workflow.compile()