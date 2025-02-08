from src.models import trending_topic_state
from src.nodes import trending_topic, search_articles, summarize_article, data_enrichment, user_feedback, final_output
from langgraph.graph import StateGraph, START, END

def create_graph():
    graph = StateGraph(trending_topic_state)
    graph.add_node('trending_topic', trending_topic)
    graph.add_node('search_articles', search_articles)
    graph.add_node('summarize_article', summarize_article)
    graph.add_node('data_enrichment', data_enrichment)
    graph.add_node('user_feedback', user_feedback)
    graph.add_node('final_output', final_output)
    graph.add_edge(START, 'trending_topic')
    graph.add_edge('trending_topic', 'search_articles')
    graph.add_edge('search_articles', 'data_enrichment')
    graph.add_edge('data_enrichment', 'summarize_article')
    graph.add_edge('summarize_article', 'user_feedback')
    graph.add_edge('user_feedback', 'final_output')
    graph.add_edge('final_output', END)
    return graph