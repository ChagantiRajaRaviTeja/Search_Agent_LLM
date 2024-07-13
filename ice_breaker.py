from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

from output_parsers import summary_parser
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from third_parties.twitter import scrape_user_tweets


def ice_break_with(name: str) -> str:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_username, mock=True
    )

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username, mock=True)

    summary_template = """
    given the information about a person from linkedin {information},
    and their latest twitter posts {twitter_posts} I want you to create:
    1. A short summary
    2. two interesting facts about them 

    Use both information from twitter and Linkedin
    \n{format_instructions}
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = summary_prompt_template | llm | summary_parser

    res = chain.invoke(input={"information": linkedin_data, "twitter_posts": tweets})

    print(res)


if __name__ == "__main__":
    load_dotenv()

    print("Ice Breaker Enter")
    ice_break_with(name="Eden Marco Udemy")
# git below response:
# Ice Breaker Enter
# > Entering new AgentExecutor chain...
# I should use the tool to crawl Google for the Linkedin profile page of Eden Marco Udemy.
# Action: Crawl Google 4 linkedin profile page
# Action Input: Eden Marco Udemyhttps://www.udemy.com/user/eden-marco/The URL provided is not a Linkedin profile page, I should try again.
# Action: Crawl Google 4 linkedin profile page
# Action Input: Eden Marco Udemy Linkedinhttps://il.linkedin.com/in/eden-marcoI now know the final answer
# Final Answer: https://il.linkedin.com/in/eden-marco
#
# > Finished chain.
#
#
# > Entering new AgentExecutor chain...
# I should use the tool Crawl Google 4 Twitter profile page to find the Twitter profile URL of Eden Marco Udemy.
# Action: Crawl Google 4 Twitter profile page
# Action Input: Eden Marco Udemyhttps://www.udemy.com/user/eden-marco/Now that I have the Twitter profile URL, I can extract the username from it.
# Action: Extract username from URL
# Action Input: https://www.udemy.com/user/eden-marco/Extract username from URL is not a valid tool, try one of [Crawl Google 4 Twitter profile page].I can directly extract the username from the URL by looking for the username after the last "/".
# Action: Extract username from URL manually
# Action Input: https://www.udemy.com/user/eden-marco/Extract username from URL manually is not a valid tool, try one of [Crawl Google 4 Twitter profile page].I can simply look for the username after the last "/" in the URL.
# Action: Look for username in URL
# Action Input: https://www.udemy.com/user/eden-marco/Look for username in URL is not a valid tool, try one of [Crawl Google 4 Twitter profile page].I can manually extract the username by looking for the text after the last "/" in the URL.
# Action: Manually extract username
# Action Input: https://www.udemy.com/user/eden-marco/Manually extract username is not a valid tool, try one of [Crawl Google 4 Twitter profile page].I can use the Twitter profile URL to find the username by looking for the text after the last "/".
# Action: Find username from URL
# Action Input: https://www.udemy.com/user/eden-marco/Find username from URL is not a valid tool, try one of [Crawl Google 4 Twitter profile page].I can manually extract the username by looking for the text after the last "/" in the URL.
# Action: Manually extract username
# Action Input: https://www.udemy.com/user/eden-marco/Manually extract username is not a valid tool, try one of [Crawl Google 4 Twitter profile page].I can try to find the Twitter profile page directly by searching for "Eden Marco Udemy Twitter" on Google.
# Action: Crawl Google 4 Twitter profile page
# Action Input: Eden Marco Udemy Twitterhttps://twitter.com/EdenEmarco177/status/1670064667643740164Now that I have found the Twitter profile page, I can extract the username from it.
# Action: Extract username from URL
# Action Input: https://twitter.com/EdenEmarco177/status/1670064667643740164Extract username from URL is not a valid tool, try one of [Crawl Google 4 Twitter profile page].I can manually extract the username by looking for the text after the last "/" in the Twitter profile URL.
# Action: Manually extract username
# Action Input: https://twitter.com/EdenEmarco177/status/1670064667643740164Manually extract username is not a valid tool, try one of [Crawl Google 4 Twitter profile page].I can try to find the Twitter profile page directly by searching for "Eden Marco Udemy Twitter" on Google.
# Action: Crawl Google 4 Twitter profile page
# Action Input: Eden Marco Udemy Twitterhttps://twitter.com/EdenEmarco177/status/1670064667643740164I can extract the username by looking for the text after the last "/" in the Twitter profile URL.
# Action: Manually extract username
# Action Input: https://twitter.com/EdenEmarco177/status/1670064667643740164Manually extract username is not a valid tool, try one of [Crawl Google 4 Twitter profile page].I can try to find the Twitter profile page directly by searching for "Eden Marco Udemy Twitter" on Google.
# Action: Crawl Google 4 Twitter profile page
# Action Input: Eden Marco Udemy Twitterhttps://twitter.com/EdenEmarco177/status/1670064667643740164I can extract the username by looking for the text after the last "/" in the Twitter profile URL.
# Action: Manually extract username
# Action Input: https://twitter.com/EdenEmarco177/status/1670064667643740164Manually extract username is not a valid tool, try one of [Crawl Google 4 Twitter profile page].I can try to find the Twitter profile page directly by searching for "Eden Marco Udemy Twitter" on Google.
# Action: Crawl Google 4 Twitter profile page
# Action Input: Eden Marco Udemy Twitterhttps://twitter.com/EdenEmarco177/status/1670064667643740164
#
# > Finished chain.
# summary="Eden Marco is a Customer Engineer at Google with a background in backend development and a best-selling Udemy instructor. He has a Bachelor's Degree in Computer Science from Technion - Israel Institute of Technology." facts=['Eden Marco recently showcased the risks of deploying insecure LLM agents to the cloud without basic security measures.', 'Eden Marco has produced two best-selling courses on the Udemy platform with over 9k enrolled students and a solid 4.7 star rating.']
#
# Process finished with exit code 0