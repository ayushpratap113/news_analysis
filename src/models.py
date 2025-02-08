from typing import List, Optional
from pydantic import BaseModel, Field

class topic(BaseModel):
    topic_heading: str = Field(description="The topic of article", example="Cisco: Securing enterprises in the AI era")
    date: str = Field(description="The date of article", example="15 January 2025")
    @property
    def persona(self) -> str:
        return f"Topic: {self.topic_heading}\n Date: {self.date}\n"

class llm_topic_output(BaseModel):
    topics: List[topic] = Field(description="list of topics with topic_heading and date")

class Search_results(BaseModel):
    result: str = Field(description="content of search results for the topic")
    source: str = Field(description="sources or urls of search results for the topic")

class trending_topic_state(BaseModel):
    curr_date: Optional[str] = ""
    urls: List[str]
    topics: Optional[List[topic]] = []
    results: Optional[List[Search_results]] = []
    report: Optional[str] = ""
    feedback: Optional[str] = ""