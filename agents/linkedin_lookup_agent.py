import os

from langchain import (
    hub,
)  # we use hub to download pre-made prompts that are made by the langchain team and langchain community
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)  # we're using ReAct agent(Reasoning-and-Acting)
from langchain_core.tools import (
    Tool,
)  # tools are interfaces that help our langchain agents interact with external world
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv
from tools.tools import get_profile_url_tavily

load_dotenv()


def lookup(name: str) -> str:
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo",
        openai_api_key=os.environ["OPENAI_API_KEY"],
    )
    template = """given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
                          Your answer should contain only a URL"""

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the Linkedin Page URL",
        )
    ]  # list of tools we're providing for agent. Here only one tool for our case.
    # description field in Tool is very important, because that's what tells LLM whether to use a particular tool or not

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(
        agent=agent, tools=tools_for_agent, verbose=True
    )  # providing Runtime for agent to run in loops

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linked_profile_url = result["output"]
    return linked_profile_url


if __name__ == "__main__":
    print(
        lookup(name="Linkedin Chaganti Ravi Teja ")
    )  # Prompting for my linkedin info using my name
    # got response after few iterations:"url": "https://in.linkedin.com/in/chaganti-ravi-teja-533276217",
    # my url is fourth in the list of responses from Tavily API
