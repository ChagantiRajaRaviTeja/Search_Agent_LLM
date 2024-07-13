import os

from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv


def get_profile_url_tavily(name: str):
    """Searches for Linkedin or Twitter Profile Page."""
    search = TavilySearchResults()
    res = search.run(f"{name}")
    print(res)
    return res[0]["url"]
# if __name__=="__main__":
#     load_dotenv()
#     print(os.environ['TAVILY_API_KEY'])
#     result = get_profile_url_tavily(name = "Linkedin Eden Marco")
#     print(result)