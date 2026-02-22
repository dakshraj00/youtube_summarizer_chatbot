from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict,Annotated,List
from pydantic import BaseModel
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode,tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from  my_tools import get_summary
from web_ser_tool import web_search

load_dotenv()
llm=ChatOpenAI(streaming=True)
thread_id='1'

CONFIG={'configurable':{"thread_id":thread_id}}
# search_tool=DuckDuckGoSearchRun(region='us-en')
# get_summary=get_summary()
tools=[get_summary,web_search]
llm_with_tools=llm.bind_tools(tools)

class chat_state(TypedDict):
    messages:Annotated[List[BaseMessage],add_messages]

def chat_node(state:chat_state):
    messages=state['messages']
    response=llm_with_tools.invoke(messages)

    return {'messages':[response]}

checkpointer=MemorySaver()
graph=StateGraph(chat_state)

tool_node=ToolNode(tools)

graph.add_node("chat_node",chat_node)
graph.add_node('tools',tool_node)

graph.add_edge(START,"chat_node")
graph.add_conditional_edges("chat_node",tools_condition)
# graph.add_edge("chat_node",END)
graph.add_edge('tools',"chat_node")
model=graph.compile(checkpointer=checkpointer)
