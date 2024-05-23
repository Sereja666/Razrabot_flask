from datetime import datetime


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
from sqlalchemy.engine.reflection import Inspector
from config import settings




def create_table():
    engine = create_engine(settings.db_url)
    metadata = MetaData()

    tasks = Table('task', metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('title', String(100), nullable=False),
        Column('description', String(200)),
        Column('created_at', DateTime, default=datetime.utcnow),
        Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    )

    metadata.create_all(engine)


create_table()