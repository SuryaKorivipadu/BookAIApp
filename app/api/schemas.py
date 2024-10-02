from uuid import UUID
from pydantic import BaseModel, ConfigDict

#schema for returning a book
class book(BaseModel):
    year_published: int
    title: str
    author: str
    genre: str
    summary: str
    model_config = ConfigDict(
        from_attributes= True,
        json_schema_extra={
            "example":{
                "year_published": 2001,
                "title":"Sample content",
                "author":"Sample content",
                "genre":"Sample content",
                "summary" : "Sample content"
            }
        }
    )

class review(BaseModel):
    user_id: int
    rating: int
    review_text: str
    book_id: str
    model_config = ConfigDict(
        from_attributes= True,
        json_schema_extra={
            "example":{
                "user_id":1,
                "rating":1,
                "review_text" : "Sample content",
                "book_id": "1"
            }
        }
    )