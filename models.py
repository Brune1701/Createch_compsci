#contains pydantic models for structures and data

from pydantic import BaseModel, Field


class Article(BaseModel):
    name: str = Field(                                    #name
        description="The name of the article",
        examples=["Alphabet"]
    )
    content: str = Field(                                 #HTML
        description="Content in HTML of the article"
    )
    articleUrl: str                                       #URL
    source: str = Field(                                  #markdown
        description="Content in Markdown of the article"
    )


class ArticleDetail(BaseModel):
    content: str
    source: str


class ArticleInfo(BaseModel):
    name: str
    articleUrl: str


# Modèle pour créer un article

class ArticleCreate(BaseModel):
    name: str
    content: str


#Model that creates a comments 

class CommentCreate(BaseModel):
    content: str = Field(min_length=1)
    author: str | None = None


class Comment(CommentCreate):
    id: int
