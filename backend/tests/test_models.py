"""Test database models without database connection."""

from datetime import datetime

from app.db.models import Article, ArticleTag, NewsSource, Tag, User, UserPreference


def test_user_model_creation():
    """Test User model can be created."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_password_here",
        is_active=True,
        is_superuser=False
    )

    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.is_active is True
    assert user.is_superuser is False


def test_news_source_model():
    """Test NewsSource model can be created."""
    source = NewsSource(
        name="Test News",
        url="https://testnews.com",
        rss_url="https://testnews.com/rss",
        is_active=True,
        category="technology"
    )

    assert source.name == "Test News"
    assert source.url == "https://testnews.com"
    assert source.category == "technology"
    assert source.is_active is True


def test_article_model():
    """Test Article model can be created."""
    article = Article(
        title="Test Article",
        url="https://example.com/article",
        content="This is test content",
        summary="This is a summary",
        author="Test Author",
        published_at=datetime.now(),
        is_processed=False,
        sentiment_score=0.5,
        source_id=1
    )

    assert article.title == "Test Article"
    assert article.author == "Test Author"
    assert article.is_processed is False
    assert article.sentiment_score == 0.5


def test_tag_model():
    """Test Tag model can be created."""
    tag = Tag(name="python")

    assert tag.name == "python"


def test_article_tag_model():
    """Test ArticleTag model can be created."""
    article_tag = ArticleTag(
        article_id=1,
        tag_id=1,
        confidence=0.95
    )

    assert article_tag.article_id == 1
    assert article_tag.tag_id == 1
    assert article_tag.confidence == 0.95


def test_user_preference_model():
    """Test UserPreference model can be created."""
    preference = UserPreference(
        user_id=1,
        preference_type="category",
        preference_value="technology",
        weight=1.0
    )

    assert preference.user_id == 1
    assert preference.preference_type == "category"
    assert preference.preference_value == "technology"
    assert preference.weight == 1.0
