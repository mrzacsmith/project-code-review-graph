import os
from typing import List, Dict, TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, Graph
from dotenv import load_dotenv

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY2")

class State(TypedDict):
    current_file: str
    reviewed_files: List[str]
    reviews: Dict[str, str]
    root_folder: str
    files_remaining: bool

llm = ChatOpenAI(api_key=openai_key, model="gpt-4o-mini")

workflow = StateGraph(State)

def traverse_files(state: State):
    root_folder = state["root_folder"]
    all_files = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith(('.py', '.js')):
                all_files.append(os.path.join(root, file))
    
    if not all_files and not state["reviewed_files"]:
        state["files_remaining"] = False
        state["current_file"] = ""
        return state
    
    if not state["reviewed_files"]:
        state["current_file"] = all_files[0]
        state["reviewed_files"] = all_files[1:]
    elif state["reviewed_files"]:
        state["current_file"] = state["reviewed_files"].pop(0)
    else:
        state["files_remaining"] = False
        state["current_file"] = ""
        return state
    
    state["files_remaining"] = bool(state["reviewed_files"])
    return state

def review_code(state: State):
    with open(state["current_file"], 'r') as file:
        content = file.read()
    
    prompt = f"""
    Review the following code file and provide a brief summary of its purpose and its connections to other files:

    File: {state["current_file"]}

    Content:
    {content}

    Summary:
    """

    review = llm(prompt)
    state["reviews"][state["current_file"]] = review
    return state

def generate_markdown(state: State):
    file_path = "code_review_summary.md"
    
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("# Code Review Summary\n\n")
    
    with open(file_path, "a") as f:
        file = state["current_file"]
        review = state["reviews"][file]
        # print(f"REVIEW REVIEW: {review.content}")
        f.write(f"## {file}\n\n{review.content}\n\n")
    
    return state
      
def end_state(state: State):
    return state

workflow.add_node("traverse", traverse_files)
workflow.add_node("review", review_code)
workflow.add_node("generate", generate_markdown)
workflow.add_node("end", end_state)


workflow.add_conditional_edges(
    "traverse",
    lambda x: "review" if x["files_remaining"] else "end"
)
workflow.add_edge("review", "generate")
workflow.add_conditional_edges(
    "generate",
    lambda x: "traverse" if x["files_remaining"] else "end"
)

workflow.set_entry_point("traverse")
workflow.set_finish_point("end")

graph = workflow.compile()

initial_state = {
    "current_file": "",
    "reviewed_files": [],
    "reviews": {},
    "root_folder": "/Users/codeshock/software/code-shock/lead-magnet/src",
    "files_remaining": True
}

try:
    for state in graph.stream(initial_state):
        print(f"Current state: {state}")
        if 'traverse' in state:
            traverse_state = state['traverse']
            # print(f"Current file: {traverse_state.get('current_file', 'No file')}")
            print(f"Files remaining: {traverse_state.get('files_remaining', False)}")
        else:
            print("Unexpected state structure:", state)
        print("---")
except Exception as e:
    print(f"An error occurred: {str(e)}")
    import traceback
    traceback.print_exc()

