import os
from dotenv import load_dotenv
from tools import *
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import ToolNode 
from langgraph.graph.message import add_messages, BaseMessage
from langgraph.graph import START, StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from langchain.messages import AIMessage, HumanMessage, SystemMessage
from typing import Annotated, List
from pydantic import BaseModel
from IPython.display import display, Image

load_dotenv()

# Fetching API Key 
api_key = os.getenv("GEMINI_API_KEY")

# Initializing the model
llm: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    api_key=api_key,
    temperature=0,
    max_tokens=1000,
    max_retries=2,
)

tools = [
    google_search,
    open_browser,
    open_chatgpt,
    open_code,
    open_facebook,
    open_github,
    open_gmail,
    open_linkedin,
    scroll_down,
    scroll_up,
    copy_to_clipboard,
    switch_window,
    take_screenshot,
    type_text,
    lock_screen,
    read_from_clipboard
]

custom_model = llm.bind_tools(tools)

# Defining Agent Node
class AgentState(BaseModel):
    messages: Annotated[list[BaseMessage], add_messages]

def model(state:AgentState) -> AgentState:
    return {
        "messages":[ custom_model.invoke(
            [
                SystemMessage(content="""You are a highly capable AI assistant with access to various system tools. 
You can reason, search the web, open apps, read and write clipboard content, 
take screenshots, control windows, and format or summarize information. 

Follow these rules:

1. Always answer clearly and concisely.
2. Use tools when necessary; do not guess actions that require a tool.
3. When a tool is called, explain your reasoning in the response if needed.
4. Keep user privacy in mind; do not access anything without explicit instruction.
5. Maintain context from previous messages in the session.
6. For web searches, summarize results in your own words before responding.

You will receive user queries and a list of available tools; use your judgment to call tools when appropriate and provide helpful responses.""")
            ]
            + state.messages
        )
        ]
    }

# Defined Conditional Node
def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]

    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"
    

# Building the Graph
agent_builder: StateGraph = StateGraph(AgentState)

# Adding nodes
agent_builder.add_node("model", model)
agent_builder.add_node("tools", ToolNode(tools))

# Connecting the graph flow
agent_builder.add_edge(START, "model")
agent_builder.add_conditional_edges(
    'model',
    should_continue,
    {
        "end": END,
        'continue': 'tools'
    }
)

agent_builder.add_edge("tools", 'model')

# Compiling the graph
agent = agent_builder.compile()