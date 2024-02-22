from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine
from config import host, user, password, dbname, port


engine = create_async_engine(f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}', echo=True)
metadata = MetaData()
