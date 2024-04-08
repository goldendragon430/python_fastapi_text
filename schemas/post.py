from typing import Optional
from pydantic import BaseModel

class Post(BaseModel):
    id: Optional[int]
    text: str
    user_id: Optional[int]