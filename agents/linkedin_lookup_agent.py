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
        lookup(name="Linkedin Chaganti Ravi Teja kanpur ")
    )  # Prompting for my linkedin info using my name
    # got response:
    # > Entering new AgentExecutor chain...
    # I should use the tool to crawl Google for the Linkedin profile page of Chaganti Ravi Teja Kanpur.
    # Action: Crawl Google 4 linkedin profile page
    # Action Input: name='Chaganti Ravi Teja Kanpur'[{'url': 'https://in.linkedin.com/in/chaganti-ravi-teja-533276217', 'content': "View Chaganti Ravi Teja's profile on LinkedIn, the world's largest professional community. Chaganti's education is listed on their profile. See the complete profile on LinkedIn and discover Chaganti's connections and jobs at similar companies. ... Our thought leaders at IIT Kanpur are driving the change in science and innovation. Happy ..."}, {'url': 'https://www.linkedin.com/in/ravi-teja-chaganti-35b791167', 'content': 'MS Student at Indian Institute of Technology, Kanpur Guntur. Connect ... Others named Ravi Teja Chaganti. RAVI TEJA CHAGANTI ASM Andhra Pradesh, India. Ravi Teja Reddy Chaganti ...'}, {'url': 'https://www.linkedin.com/posts/chaganti-ravi-teja-533276217_iitkanpur-technology-smartdevices-activity-6937612652231692288-2WyG', 'content': 'Chaganti Ravi Teja posted images on LinkedIn. Secretary, Department of Science & Technology. On Lien from Professor, Department of EE, IIT Bombay.'}, {'url': 'https://www.linkedin.com/pub/dir/Chaganti/Ravi', 'content': 'There are 3 professionals named "Chaganti Ravi", who use LinkedIn to exchange information, ideas, and opportunities. ... Chaganti Ravi Teja MS Student at Indian Institute of Technology, Kanpur ...'}, {'url': 'https://www.facebook.com/ravi.chaganti.teja/', 'content': 'Ravi Teja Chaganti is on Facebook. Join Facebook to connect with Ravi Teja Chaganti and others you may know. Facebook gives people the power to share and makes the world more open and connected.'}]
    # https://in.linkedin.com/in/chaganti-ravi-teja-533276217I now know the final answer
    # Final Answer: https://in.linkedin.com/in/chaganti-ravi-teja-533276217
    #
    # > Finished chain.
    # https://in.linkedin.com/in/chaganti-ravi-teja-533276217
    #
    # Process finished with exit code 0
