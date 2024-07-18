# This code snippet contains basic prompting the LLM
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI

if __name__ == "__main__":
    load_dotenv()  # to load environment variables(in this case for API_KEY)

    print("Hello LangChain")
    information = """
        Avul Pakir Jainulabdeen Abdul Kalam BR (/ˈəbdʊl kəˈlɑːm/ ⓘ; 15 October 1931 – 27 July 2015) was an Indian aerospace scientist and statesman who served as the 11th president of India from 2002 to 2007. Born and raised in a Muslim family in Rameswaram, Tamil Nadu, he studied physics and aerospace engineering. He spent the next four decades as a scientist and science administrator, mainly at the Defence Research and Development Organisation (DRDO) and Indian Space Research Organisation (ISRO) and was intimately involved in India's civilian space programme and military missile development efforts.[1] He thus came to be known as the Missile Man of India for his work on the development of ballistic missile and launch vehicle technology.[2][3][4] He also played a pivotal organisational, technical, and political role in India's Pokhran-II nuclear tests in 1998, the first since the original nuclear test by India in 1974.[5]

Kalam was elected as the 11th president of India in 2002 with the support of both the ruling Bharatiya Janata Party and the then-opposition Indian National Congress. Widely referred to as the "People's President",[6] he returned to his civilian life of education, writing and public service after a single term. He was a recipient of several prestigious awards, including the Bharat Ratna, India's highest civilian honour.
    """
    # copied first 2 paragraphs from Dr. Kalam's wikipedia page
    # creating a prompt
    summary_template = """
    given the information {info} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    """
    # creating prompt template
    summary_prompt_template = PromptTemplate(
        input_variables=["info"], template=summary_template
    )
    # input_variables field should be populated with list, because we can have multiple inputs for a prompt(like {"info"} {"context"} {"topic"} etc in prompt)

    llm = ChatOpenAI(
        temperature=0, model_name="gpt-3.5-turbo"
    )  # temperature=0 means no creativity expected from LLM
    # creating chain
    chain = summary_prompt_template | llm
    res = chain.invoke(input={"info": information})
    print(res)
    # Got response: content="1. Avul Pakir Jainulabdeen Abdul Kalam BR was an Indian aerospace scientist and statesman who served as the 11th president of India from 2002 to 2007. Known as the Missile Man of India, he played a key role in India's civilian space programme, military missile development efforts, and the Pokhran-II nuclear tests.\n\n2. Two interesting facts about Abdul Kalam:\n- He was the first scientist to hold the position of President of India.\n- Despite his scientific background, Kalam was also a prolific writer and authored several books on topics ranging from nuclear physics to spiritualism." response_metadata={'token_usage': {'completion_tokens': 127, 'prompt_tokens': 358, 'total_tokens': 485}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-76f21b6e-df1e-454c-9797-0e3595ddb339-0' usage_metadata={'input_tokens': 358, 'output_tokens': 127, 'total_tokens': 485}
