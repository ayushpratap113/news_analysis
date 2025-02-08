from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.document_loaders import UnstructuredURLLoader

tavily_search_tool = TavilySearchResults(max_results=3, include_answer=True, include_raw_content=True)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, verbose=True)