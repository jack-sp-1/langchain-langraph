from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from tavily import TavilyClient
load_dotenv()

tavily = TavilyClient()
@tool
def search(query:str)->str:
    """Tool for searching on the internet
    Args:
        query:query to search for
    Returns:
        the search result""" 
    print(f"searching for {query}")
    return tavily.search(query=query)

llm = ChatOllama(model="gpt-oss:latest",temperature = 0.7,
    max_tokens = 100,
    context_window=8000)
tools = [search]
agent = create_agent(model=llm,tools=tools)
    
def main():
    print("hello from langchain")
    result = agent.invoke({"messages":HumanMessage(content="what is the weather  in Tokyo")})
    print(result)

if __name__ == "__main__":
    main()    