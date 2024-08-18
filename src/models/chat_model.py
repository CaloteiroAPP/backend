from pydantic import BaseModel

from src.models.message_model import Message


class Chat(BaseModel):
    blocked: bool = False
    messages: list[Message] = []