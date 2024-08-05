# AI Project Code Review Tool

## Function
This tool is an AI-powered code review assistant that recursively analyzes code files in a specified directory. It performs the following tasks:

1. Traverses through a root folder and its subfolders to find code files.
2. Uses an AI language model to review each code file.
3. Generates a summary of each file's purpose and its connections to other files.
4. Writes these reviews to a markdown file, appending new reviews to the end.

The tool is designed to work with various code file types (e.g., .py, .js, .java, .cpp) and can be easily extended to support additional file extensions.

## Required Packages
To run this tool, you need to install the following Python packages:

1. langgraph: For creating and managing the workflow graph.
   ```
   pip install langgraph
   ```

2. langchain: For interfacing with language models.
   ```
   pip install langchain
   ```

3. openai: For accessing the OpenAI API (used by langchain).
   ```
   pip install openai
   ```

4. tkinter: For the file dialog (usually comes pre-installed with Python).

## Additional Requirements
- An OpenAI API key is required. Set this as an environment variable named `OPENAI_API_KEY`.

## Usage
1. Ensure all required packages are installed.
2. Set up your OpenAI API key in your environment variables.
3. Run the script. A file dialog will open for you to select the root folder to review.
4. The tool will process all code files and generate a `code_review_summary.md` file with the AI-generated reviews.

Note: The specific file extensions to be reviewed can be modified in the `traverse_files` function.
