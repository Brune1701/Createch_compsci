
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
ARTICLES_DIR = Path(__file__).resolve().parent.parent / "articles"

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_methods=["*"],
allow_headers=["*"],
)

@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello CreaTech!"}

@app.get("/list")
def list_article() -> list[dict[str, str]]:
    articles = []
    for a in ARTICLES_DIR.rglob("*.md"):
        articles.append({"name": a.stem.replace("_", " "), "articleUrl": a.stem})
    return articles

@app.get("/article/{articleUrl}")
def read_article(articleUrl: str) -> dict[str, str]:
    article_path = (ARTICLES_DIR / f"{articleUrl}.md").resolve()
    source = article_path.read_text(encoding="utf-8")
    return {
        "name": article_path.stem.replace("_", " "),
        "articleUrl": article_path.stem,
        "content": markdowner.convert(source),
        "source": source,
    }


