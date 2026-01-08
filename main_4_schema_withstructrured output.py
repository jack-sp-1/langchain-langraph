from dotenv import load_dotenv

load_dotenv()

from langchain_classic import hub
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents.react.agent import create_react_agent
from langchain_core.output_parsers.pydantic import PydanticOutputParser #output from llm(json) to pydangtic class 
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda#lanchain expressionlangueage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS
from schemas import AgentResponse

tools = [TavilySearch()]
llm = ChatOpenAI(model="gpt-4") #gpt-5 gives respones as error due to stop variable.
structured_llm = llm.with_structured_output(AgentResponse) #function calling
react_prompt = hub.pull("hwchase17/react")
output_parser = PydanticOutputParser(pydantic_object=AgentResponse) #output_parser.parse(result["output"])
react_prompt_with_format_instructions = PromptTemplate(
    template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
    input_variables=["input", "agent_scratchpad", "tool_names"],
).partial(format_instructions="")
#partial   will have both the values which are available and not available.

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=react_prompt_with_format_instructions,
)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)  #this returns json from LLM and agentexecutor is like a loop
extract_output = RunnableLambda(lambda x: x["output"]) #this gives json which will be converted to pydantic object
##parse_output = RunnableLambda(lambda x: output_parser.parse(x))  #lambda function into a runnable langchain(custom logic) and it isinvokable
chain = agent_executor | extract_output | structured_llm
#chain = agent_executor

def main():
    result = chain.invoke(
        input={
            "input": "search for 3 job postings for an ai engineer using langchain in the bay area on linkedin and list their details",
        }
    )
    print(result)


if __name__ == "__main__":
    main()