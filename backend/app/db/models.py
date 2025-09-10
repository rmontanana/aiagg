from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class User(Base):
    """User model for authentication and preferences."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    preferences = relationship("UserPreference", back_populates="user")


class NewsSource(Base):
    """News source configuration."""
    __tablename__ = "news_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    rss_url = Column(String)
    is_active = Column(Boolean, default=True)
    category = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    articles = relationship("Article", back_populates="source")


class Article(Base):
    """News article model."""
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    url = Column(String, nullable=False, unique=True)
    content = Column(Text)
    summary = Column(Text)
    author = Column(String)
    published_at = Column(DateTime(timezone=True))
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())
    is_processed = Column(Boolean, default=False)
    sentiment_score = Column(Float)

    # Foreign keys
    source_id = Column(Integer, ForeignKey("news_sources.id"), nullable=False)

    # Relationships
    source = relationship("NewsSource", back_populates="articles")
    tags = relationship("ArticleTag", back_populates="article")


class Tag(Base):
    """Content tags for categorization."""
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    articles = relationship("ArticleTag", back_populates="tag")


class ArticleTag(Base):
    """Many-to-many relationship between articles and tags."""
    __tablename__ = "article_tags"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False)
    confidence = Column(Float, default=1.0)

    # Relationships
    article = relationship("Article", back_populates="tags")
    tag = relationship("Tag", back_populates="articles")


class UserPreference(Base):
    """User preferences for content personalization."""
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    preference_type = Column(String, nullable=False)  # 'category', 'source', 'keyword'
    preference_value = Column(String, nullable=False)
    weight = Column(Float, default=1.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="preferences")
