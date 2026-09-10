
from pathlib import Path

import markdown
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from models import Comment, CommentCreate


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


ARTICLES_DIR = Path(__file__).resolve().parent.parent / "articles"
TRASH_DIR = Path(__file__).resolve().parent.parent / "trash"

ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
TRASH_DIR.mkdir(parents=True, exist_ok=True)


class ArticleInfo(BaseModel):
    name: str
    articleUrl: str


class Article(BaseModel):
    name: str = Field(
        description="The name of the article",
        examples=["Alphabet"]
    )
    content: str = Field(
        description="Content in HTML of the article"
    )
    articleUrl: str
    source: str = Field(
        description="Content in Markdown of the article"
    )


class ArticleCreate(BaseModel):
    name: str
    content: str


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/list", response_model=list[ArticleInfo])
def list_articles() -> list[ArticleInfo]:
    articles = []

    for article_path in ARTICLES_DIR.glob("*.md"):
        articles.append(
            ArticleInfo(
                name=article_path.stem.replace("_", " "),
                articleUrl=article_path.stem
            )
        )

    return articles


@app.get("/article/{articleurl}", response_model=Article)
def read_article(articleurl: str) -> Article:
    if (
        ".." in articleurl
        or "/" in articleurl
        or "\\" in articleurl
    ):
        raise HTTPException(
            status_code=404,
            detail="The article does not exist."
        )

    article_path = ARTICLES_DIR / f"{articleurl}.md"

    if not article_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="The article does not exist."
        )

    source = article_path.read_text(encoding="utf-8")
    content = markdown.markdown(source)
    name = articleurl.replace("_", " ")

    return Article(
        name=name,
        content=content,
        articleUrl=articleurl,
        source=source
    )


@app.get("/article/{articleurl}/delete")
def delete_article(articleurl: str) -> dict[str, bool]:
    if (
        ".." in articleurl
        or "/" in articleurl
        or "\\" in articleurl
    ):
        raise HTTPException(
            status_code=404,
            detail="The article does not exist."
        )

    source = ARTICLES_DIR / f"{articleurl}.md"
    destination = TRASH_DIR / source.name

    if not source.is_file():
        raise HTTPException(
            status_code=404,
            detail="The article does not exist."
        )

    if destination.exists():
        destination.unlink()

    source.rename(destination)

    return {"deleted": True}


@app.post("/create", response_model=Article)
def create_article(article: ArticleCreate) -> Article:
    filename = article.name.strip().replace(" ", "_")

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="Article name cannot be empty."
        )

    if (
        ".." in filename
        or "/" in filename
        or "\\" in filename
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid article name."
        )

    new_article_file = ARTICLES_DIR / f"{filename}.md"

    if new_article_file.exists():
        raise HTTPException(
            status_code=409,
            detail="The article already exists."
        )

    new_article_file.write_text(
        article.content,
        encoding="utf-8"
    )

    content = markdown.markdown(article.content)

    return Article(
        name=article.name,
        articleUrl=filename,
        content=content,
        source=article.content
    )


comments: list[Comment] = []
next_comment_id = 1


@app.get("/comments", response_model=list[Comment])
def list_comments() -> list[Comment]:
    return comments


@app.post("/comments", response_model=Comment)
def create_comment(comment: CommentCreate) -> Comment:
    global next_comment_id

    new_comment = Comment(
        id=next_comment_id,
        author=comment.author,
        content=comment.content
    )

    comments.append(new_comment)
    next_comment_id += 1

    return new_comment 

