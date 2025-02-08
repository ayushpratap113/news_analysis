import streamlit as st
from src.config import _set_env
from src.graph import create_graph
from src.models import trending_topic_state
from IPython.display import Image, display, Markdown

# Set environment variables
_set_env("OPENAI_API_KEY")
_set_env("TAVILY_API_KEY")
_set_env("LANGCHAIN_API_KEY")

# Streamlit UI
st.title("AI News Trending Topics")

urls = st.text_input("Enter URLs (comma separated)", "https://www.artificialintelligence-news.com/")
urls_list = [url.strip() for url in urls.split(",")]

if st.button("Generate Report"):
    graph = create_graph()
    graph = graph.compile()
    state = graph.invoke(trending_topic_state(urls=urls_list))
    st.markdown(state['report'])

# For running as a script
if __name__ == "__main__":
    graph = create_graph()
    graph = graph.compile()
    display(Image(graph.get_graph(xray=1).draw_mermaid_png()))

    urls = ['https://www.artificialintelligence-news.com/']
    state = graph.invoke(trending_topic_state(urls=urls))
    display(Markdown(state['report']))