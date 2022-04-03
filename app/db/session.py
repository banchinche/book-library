from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URI)
async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False,
)
