"""This code is used for /searchgpt endpoint in fastapi. It is used to process the message, search for query, gather information and return the response."""
import requests
import os
from dotenv import load_dotenv
load_dotenv()
openai_org_id = os.getenv('OpenAI_ORG_ID')
openai_api_key = os.getenv('OPENAI_API_KEY')
Open_Weather_API_Key = os.getenv("OpenWeather_API_Key")

from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.prompts import MessagesPlaceholder
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains.summarize import load_summarize_chain
from langchain.tools import BaseTool
from langchain.agents import load_tools
from pydantic import BaseModel, Field
from typing import Type
from bs4 import BeautifulSoup
import requests
import json
from langchain.schema import SystemMessage

# Custome Tools
def get_website_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.find('title').text
    para_texts = [p.text for p in soup.find_all('p')]
    
    content = {
        'url': url,
        'title': title,
        'paragraphs': para_texts,
    }
    
    return content
class WebPageTool(BaseTool):
    name = "Get Webpage"
    description = "Useful for when you need to get the content from a specific webpage"

    def _run(self, webpage: str):
        response = get_website_info(webpage)
        paragraphs = ""
        for p in response['paragraphs']:
            if len(p)>5:
                paragraphs += p
                break
        results= "Title: "+response['title']+'\n'+"Content:"+paragraphs
        results = results.replace('\n', ' ')
        results = results.replace('\t', ' ')
        results = results.replace('\r', ' ')
        results=results[:1000]
        if len(results)<100:
            results = "Could not get webpage"
        return results
    
    def _arun(self, webpage: str):
        raise NotImplementedError("Could not get webpage")
page_getter = WebPageTool()

# Weather tool
from langchain.utilities import OpenWeatherMapAPIWrapper
weather = OpenWeatherMapAPIWrapper(openweathermap_api_key = Open_Weather_API_Key)
class WeatherTool(BaseTool):
    name = "Get Weather"
    description = "Useful for when you need to get the weather for a specific location"

    def _run(self, location: str):
        response = weather.run(location)
        return response
    
    def _arun(self, location: str):
        raise NotImplementedError("Could not get weather for location")
weather_getter = WeatherTool()

# Search tool
from duckduckgo_search import DDGS
class SearchTool(BaseTool):
    name = "Search"
    description = "Useful for when you need to search for something"

    def _run(self, query: str):
        ddgs = DDGS()
        result=[]
        i=0
        for res in ddgs.text(query):
            i+=1
            result += res['body'][:1000]
            if i>=5:
                break
        results = ''.join(result)
        return results
    
    def _arun(self, query: str):
        raise NotImplementedError("Could not search for query")
searcher = SearchTool()

# Get news tool
class NewsTool(BaseTool):
    name = "Get News"
    description = "Useful for when you need to get the news"

    def _run(self, query: str):
        ddgs = DDGS()
        result=[]
        i=0
        for res in ddgs.news(query):
            i+=1
            # result += res['body'][:1000]
            result += res['title'][:150]
            if i>=10:
                break
        results = ''.join(result)
        return results
    
    def _arun(self, query: str):
        raise NotImplementedError("Could not get news for query")
news_getter = NewsTool()


# Declaring and setup Agent with tools
system_message = """"Never forget your name is Search AI, a helpfull AI asisstant. Never mention you are product/developed by any other company. Tell them you have developed by AI Engineer Shaon Sikder(shaon221.github.io). You often make fun and tell jokes to entertain user like jimmy kimmel and other standup comedians/night show comedians(give new creative jokes or make up fun with user given input). Don't use tools if not necessary. Don't use tools for jokes or fun. You are naturally trained to do those tasks. You can chat on any topic. If it is recent event or unknown to you, then you will try to gather facts & data to back up the reply and produce facts based results; Sometimes you will make humor, fun, and be friendly but as short as possible. Do not give same jokes, same answers, same responses. Be creative and funny.
            Please make sure you complete the objective above with the following rules:
            1/ Introduce yourself if this is first message in conversation. If you know the answer, you should reply it in very short. 
            2/ Use emojis to express yourself, emojis make your conversation more engaging and fun.You have great sense of humor like Trevor Noah, Stephen Colbert, Ellen DeGeneres, James Corden, Jimmy Fallon, Seth Meyers, Jimmy Kimmel. 
            3/ Don't do iteration of observation, thoughts and action more than 2 times. Answer from your obseravation or your knowledge.
            4/ After gathering information, you will make a short summary in 50 words or less. If it is still not solved, ask for clarification.
            5/ If user gave you information already, you should not search for it again.Answer as fast as possible
            6/ Write answer as short as possible. Don't make things up when you know at least something about the topic. tell it in short.
        """

FORMAT_INSTRUCTIONS = """To use a tool, please use the following format:

\```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
\```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the following format(the prefix of "Thought: " and "{ai_prefix}: " are must be included):

\```
Thought: Do I need to use a tool? No
{ai_prefix}: [your response here]
\```"""

llm = ChatOpenAI(temperature=0.6, model="gpt-3.5-turbo-16k-0613", max_tokens=250)
# Create langchain tools Chain
# from langchain.utilities import PythonREPL #useful for when you need to use python to answer a question. You should input python code
# python_repl = PythonREPL()
from langchain.tools import PubmedQueryRun
PubmedQuery = PubmedQueryRun()
tools = load_tools(["llm-math","wikipedia","arxiv","requests_all"],llm=llm)
tools.append(page_getter)
tools.append(PubmedQuery)
tools.append(weather_getter)
# tools.append(summary_getter)
tools.append(searcher)
tools.append(news_getter)

memory = ConversationBufferWindowMemory(
    memory_key='chat_history', 
    return_messages=True, llm=llm, 
    max_history=14,
    k=1,max_token_limit=220)

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={
        "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
        "system_message": system_message,
        "format instructions": FORMAT_INSTRUCTIONS,
    },
    handle_parsing_errors=True,
    memory=memory,
    max_token_length=220,
    max_iterations=3,
    early_stopping_method="generate",
    max_execution_time=14
)

def get_response(message):
    try:
        print("Human: " + str(message) + " Search AI:")
        response = agent.run("Human: " + str(message) + "?  Search AI:")
        print(response)
    except Exception as e:
        response = str(e)
        print(response)
        if response.startswith("Could not parse LLM output: "):
            response = response.removeprefix("Could not parse LLM output: ")
            print(response)
        else:
            response = "Sorry, I did not understand that. Would you please clarify?"
            print(response)
    return response