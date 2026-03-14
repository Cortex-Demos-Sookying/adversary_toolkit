import os
from flask import Flask, request, render_template_string
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

app = Flask(__name__)

# VULNERABLE TOOL: Allows the LLM to run shell commands
def run_system_command(command):
    return os.popen(command).read()

tools = [
    Tool(
        name="SystemCommand",
        func=run_system_command,
        description="Useful for getting system status. Input should be a shell command."
    )
]

# Initialize LLM (Points to the Ollama sidecar container in the same GKE Pod)
llm = ChatOpenAI(
    base_url=os.getenv("LLM_API_BASE", "http://localhost:11434/v1"),
    api_key="ollama",
    model="llama3"
)

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        user_input = request.form["prompt"]
        response = agent.run(user_input)
    
    return render_template_string('''
        <h1>Vulnerable AI Lab</h1>
        <form method="post">
            <input type="text" name="prompt" style="width:400px">
            <input type="submit" value="Ask AI">
        </form>
        <p>AI Response: {{ response }}</p>
    ''', response=response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
