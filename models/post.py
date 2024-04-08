from sqlalchemy import Column, Table
from sqlalchemy.sql.sqltypes import Integer, String, Text
from config.dbconnection import meta, engine

posts = Table(
    "posts",
    meta,
    Column("id", Integer, primary_key=True),
    Column(
        "text",
        Text(1024 * 1024),
    ),
    Column("user_id", Integer),
)

meta.create_all(engine)
