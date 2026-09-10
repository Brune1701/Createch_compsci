from pydantic import BaseModel, Field 

class Article(BaseModel):
    name: str =Field (description = "The name of the article", examples = ["Alphabet"])
    content : str = Field (description = "Content in HTML of the article")
    articleUrl : str 
    source : str = Field(description = "Content in Markdown of the article")

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

#Model that 

class CommentCreate(BaseModel):
    content: str = Field(min_length=1)
    author: str | None = None


class Comment(CommentCreate):
    id: int