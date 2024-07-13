from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent


def ice_break_with(name: str) -> str:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)

    summary_template = """
    given the Linkedin information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    res = chain.invoke(input={"information": linkedin_data})

    print(res["text"])
# got below response:
# 1. Chaganti Ravi Teja is a MS student at Indian Institute of Technology, Kanpur, specializing in machine learning in audio processing. He holds a Bachelor's degree in Electrical, Electronics and Communications Engineering from National Institute of Technology Hamirpur-Alumni. With a strong passion for technology and innovation, Chaganti is actively involved in the academic community and has a growing network of connections on Linkedin.

# 2. Two interesting facts about Chaganti Ravi Teja:
# - He has a keen interest in exploring the intersection of machine learning and audio processing, aiming to contribute to advancements in the field of sound technology.
# - Chaganti is from Guntur, Andhra Pradesh, India, and has a diverse educational background that has equipped him with a well-rounded skill set in engineering and technology.



if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker Enter")
    ice_break_with(name="Chaganti Ravi Teja kanpur")