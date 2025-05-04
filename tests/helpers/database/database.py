import uuid

from sqlalchemy_utils import create_database, database_exists, drop_database


def create_test_database(
    user: str,
    password: str,
    db_url_prefix: str = "test_db",
    host: str = "localhost",
    port: int = 5432,
):
    db_name = f"{db_url_prefix}_{uuid.uuid4().hex[:5]}"
    db_url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    if not database_exists(db_url):
        create_database(db_url)
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"


def drop_test_database(db_url: str):
    db_url = db_url.replace("postgresql+asyncpg", "postgresql")
    if database_exists(db_url):
        drop_database(db_url)
