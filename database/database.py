from sqlalchemy import create_engine, MetaData

from config import host, user, password, dbname, port


engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}', echo=True)
metadata = MetaData()
