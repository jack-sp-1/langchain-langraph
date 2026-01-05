from langchain_classic import hub#react function(black box)
from dotenv import load_dotenv

load_dotenv()

from langchain_classic.agents import AgentExecutor #its a for loop
from langchain_classic.agents.react.agent import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
tools  = [TavilySearch()]  #to have the searchc option for agents
llm = ChatOpenAI(model='gpt-4')

react_prompt = hub.pull("hwchase17/react")


    
agent = create_react_agent(llm=llm,tools = tools,
                           prompt=react_prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True) 

chain = agent_executor

def main():
    print("nedwone")
    result = chain.invoke(
       input={
            "input": "search for 3 job postings for an ai engineer using langchain in the bay area on linkedin and list their details",
        })
    print(result)   

#shwcchema will have all details , tool name , arguments, return value


if __name__ == "__main__":
    main()        