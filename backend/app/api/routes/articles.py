from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ...db.base import get_db
from ...db.models import Article, ArticleTag, NewsSource, Tag

router = APIRouter()


# Pydantic models
class ArticleResponse(BaseModel):
    id: int
    title: str
    url: str
    summary: str | None = None
    author: str | None = None
    published_at: datetime | None = None
    sentiment_score: float | None = None
    source_name: str
    tags: list[str] = []

    model_config = ConfigDict(from_attributes=True)


class ArticleListResponse(BaseModel):
    articles: list[ArticleResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


@router.get("/", response_model=ArticleListResponse)
async def get_articles(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    category: str | None = None,
    search: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    """Get paginated list of articles."""

    # Build query
    query = select(Article).join(NewsSource)

    # Add filters
    if category:
        query = query.where(NewsSource.category == category)

    if search:
        query = query.where(Article.title.contains(search))

    # Add ordering
    query = query.order_by(Article.published_at.desc())

    # Get total count
    count_query = select(func.count(Article.id))
    if category:
        count_query = count_query.select_from(Article.join(NewsSource)).where(NewsSource.category == category)
    if search:
        count_query = count_query.where(Article.title.contains(search))

    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Apply pagination
    offset = (page - 1) * per_page
    query = query.offset(offset).limit(per_page)

    # Execute query
    result = await db.execute(query)
    articles = result.scalars().all()

    # Transform to response model
    article_responses = []
    for article in articles:
        # Get tags for each article
        tags_result = await db.execute(
            select(Tag.name)
            .select_from(Tag.join(ArticleTag))
            .where(ArticleTag.article_id == article.id)
        )
        tags = list(tags_result.scalars().all())

        article_responses.append(ArticleResponse(
            id=article.id,
            title=article.title,
            url=article.url,
            summary=article.summary,
            author=article.author,
            published_at=article.published_at,
            sentiment_score=article.sentiment_score,
            source_name=article.source.name,
            tags=tags
        ))

    total_pages = (total + per_page - 1) // per_page

    return ArticleListResponse(
        articles=article_responses,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(
    article_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific article by ID."""

    result = await db.execute(
        select(Article).join(NewsSource).where(Article.id == article_id)
    )
    article = result.scalar_one_or_none()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # Get tags
    tags_result = await db.execute(
        select(Tag.name)
        .select_from(Tag.join(ArticleTag))
        .where(ArticleTag.article_id == article.id)
    )
    tags = list(tags_result.scalars().all())

    return ArticleResponse(
        id=article.id,
        title=article.title,
        url=article.url,
        summary=article.summary,
        author=article.author,
        published_at=article.published_at,
        sentiment_score=article.sentiment_score,
        source_name=article.source.name,
        tags=tags
    )
