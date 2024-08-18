from pydantic import BaseModel

from src.models.message_model import Message


class Chat(BaseModel):
    messages: list[Message] = []
    blocked: bool = False