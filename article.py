
#contains fonctions to read, create and handle article's files

from pathlib import Path

ARTICLES_DIR = Path(__file__).resolve().parent.parent / "articles"


def get_article_path(article_url: str) -> Path | None:
    article_path = ARTICLES_DIR / f"{article_url}.md"

    if not article_path.exists():
        return None

    return article_path


def get_articles() -> list[Path]:
    return list(ARTICLES_DIR.glob("*.md"))


#returns the article's path 

def read_article(article_url: str) -> str | None:
    article_path = get_article_path(article_url)

    if article_path is None:
        return None

    return article_path.read_text(encoding="utf-8")

#creates an article 


def create_article(article_url: str, content: str) -> None:
    article_path = ARTICLES_DIR / f"{article_url}.md"
    article_path.write_text(content, encoding="utf-8")
