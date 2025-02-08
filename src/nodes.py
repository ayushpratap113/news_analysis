from src.models import trending_topic_state, llm_topic_output, Search_results
from src.utils import tavily_search_tool, llm
from langchain_core.messages import SystemMessage
from IPython.display import Markdown, display

instructions_topic = '''
    You are tasked with extracting trending topics from the trending page data of a news website.
    Follow these instructions carefully:
    1. the data is consists of topic then a little description followed by date.
    2. Extract the topics which is between date and a description
    3. merge two topics if they are very similar
    4. choose recent 6 topics or at most 1 month old topic. Todays date is {date}.
    Here is the data you need to extract topics from:
    {data}
'''

def trending_topic(state: trending_topic_state):
    try:
        date = state.curr_date
        urls = state.urls
        data = UnstructuredURLLoader(urls=urls).load()
        structured_llm = llm.with_structured_output(llm_topic_output)
        system_message = instructions_topic.format(date=date, data=data[0].page_content)
        topics = structured_llm.invoke([SystemMessage(content=system_message)])
        return {"topics": topics.topics}
    except Exception as e:
        return {"topics": []}

instructions_search = '''
    You are tasked with summarizing the answers returned by the search engine so that next agent can create a report.
    Follow these instructions carefully:
    1. summarize the answers found here : {content}.
    2. return the summarized articles along with the source (choose only 1 most relevant source) found here : {links}.
    3. return the summarized articles along with the source as the output format.
'''

def search_articles(state: trending_topic_state):
    try:
        for topic in state.topics:
            query = topic.topic_heading + " " + topic.date
            res = tavily_search_tool.invoke({'query': query})
            content = ""
            links = []
            for r in res:
                links.append(r.get('url', ''))
            data = UnstructuredURLLoader(urls=links).load()
            for d in data:
                content += d.page_content + "\n"
            system_message = instructions_search.format(content=content, links=links)
            structured_search = llm.with_structured_output(Search_results).invoke([SystemMessage(content=system_message)])
            if isinstance(structured_search, Search_results):
                state.results.append(structured_search)
        return {}
    except Exception as e:
        return {}

summary_instructions = '''
    You are tasked with summarizing all the articles found in the search.
    Follow these instructions carefully:
    1. summarize the articles found in the list {summary}.
    2. return the summarized articles along with the sources found in {source}.
    3. each element in both list is counterpart of each other for example first item in lists summary and source constitute to one article and similarly second item in both lists constitute to another article and so on.
    4. return the summarized articles along with the source as a report in markdown format.
'''

def summarize_article(state: trending_topic_state):
    try:
        summary = []
        source = []
        for r in state.results:
            summary.append(r.result)
            source.append(r.source)
        system_message = summary_instructions.format(summary=summary, source=source)
        report = llm.invoke([SystemMessage(content=system_message)])
        state.report = report.content
        return {}
    except Exception as e:
        return {}

def final_output(state: trending_topic_state):
    try:
        display(Markdown(state.report))
        return {}
    except Exception as e:
        return {}

def error_handling(state: trending_topic_state, error: Exception):
    state.report = f"An error occurred: {str(error)}"
    return {}

def data_enrichment(state: trending_topic_state):
    try:
        enriched_data = []
        for result in state.results:
            enriched_data.append(result.result + " Additional context or metadata.")
        state.results = enriched_data
        return {}
    except Exception as e:
        return {}

def user_feedback(state: trending_topic_state):
    try:
        feedback_message = "Please provide your feedback on the generated report."
        feedback_response = input(feedback_message)
        state.feedback = feedback_response
        return {}
    except Exception as e:
        return {}