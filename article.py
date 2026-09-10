
#it returns the name of the article if its exists 

from pathlib import Path

ARTICLES_DIR = Path(__file__).resolve().parent.parent / "articles"


def get_article_path(article_url: str) -> Path | None:
    article_path = ARTICLES_DIR / f"{article_url}.md"

    if not article_path.exists():
        return None

    return article_path


def get_articles() -> list[Path]:
    return list(ARTICLES_DIR.glob("*.md"))


def read_article(article_url: str) -> str | None:
    article_path = get_article_path(article_url)

    if article_path is None:
        return None

    return article_path.read_text(encoding="utf-8")


def create_article(article_url: str, content: str) -> None:
    article_path = ARTICLES_DIR / f"{article_url}.md"
    article_path.write_text(content, encoding="utf-8")

#supprimer un article 

@app.get("/article/{articleurl}/delete")
def delete_article(articleurl: str):
    source = ARTICLES_DIR / f"{articleurl}.md"
    destination = ARTICLES_DIR.parent / "trash" / source.name

    if not source.exists():
        raise HTTPException (
            status_code=404,
            detail="The article does not exist."
        )

    if destination.exists():
        destination.unlink()

    source.rename(destination)

    return {"deleted": True}