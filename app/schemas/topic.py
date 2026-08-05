from pydantic import BaseModel


class TopicNoteItem(BaseModel):
    id: int
    title: str


class TopicResponse(BaseModel):
    cluster_id: int
    topic_name: str
    notes: list[TopicNoteItem]
