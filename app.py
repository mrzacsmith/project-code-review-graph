import os
from typing import List, Dict
from langchain_openai import OpenAI, ChatOpenAI
from langgraph.graph import StateGraph, Graph
from typing import List, Dict, TypedDict
from dotenv import load_dotenv

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY2")

# Define the state structure
class State(TypedDict):
    current_file: str
    reviewed_files: List[str]
    reviews: Dict[str, str]

# Initialize LLM
llm = ChatOpenAI(api_key=openai_key)

# Define graph
workflow = StateGraph(State)

# Define nodes 
def traverse_files(state: State):
    root_folder = "path/to/your/root/folder"
    all_files = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith(('.py', '.js', '.java', '.cpp')):  # Add more extensions as needed
                all_files.append(os.path.join(root, file))
    
    if not state["reviewed_files"]:
        state["current_file"] = all_files[0]
        state["reviewed_files"] = all_files[1:]
    elif state["reviewed_files"]:
        state["current_file"] = state["reviewed_files"].pop(0)
    else:
        return "generate"
    
    return "review"

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


#Visualize graph
def save_graph_as_png(graph: Graph, filename: str, directory: str = "."):
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)
    
    # Generate the Mermaid diagram as PNG
    png_data = graph.get_graph().draw_mermaid_png()
    
    # Create the full file path
    file_path = os.path.join(directory, filename)
    
    # Save the PNG data to a file
    with open(file_path, "wb") as f:
        f.write(png_data)
    
    print(f"Graph saved as PNG to: {file_path}")

# Usage
save_graph_as_png(graph, "workflow_diagram.png", "./")