from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine


def drop_table(table_name):
   table = Base.metadata.tables.get(table_name)
   if table is not None:
        Base.metadata.drop_all(engine, [table], checkfirst=True)
        Base.metadata.create_all(engine, [table])

def truncate_db():
    # delete all table data (but keep tables)
    # we do cleanup before test 'cause if previous test errored,
    # DB can contain dust
    meta = Base.metadata
    con = engine.connect()
    trans = con.begin()
    for table in meta.sorted_tables:
        con.execute(f'ALTER TABLE "{table.name}" DISABLE TRIGGER ALL;')
        con.execute(table.delete())
        con.execute(f'ALTER TABLE "{table.name}" ENABLE TRIGGER ALL;')
    trans.commit()


def create_db_engine(db_url: str, db_name: str, user: str, password: str, host: str, port: int = 5432) -> Engine:
    """Creates SQLAlchemy Database Engine

    Args:
        user (str): database username
        password (str): database password
        host (str): database host
        port (str): database port
        db_url (str): database url
        db_name (str): database name

    Returns:
        Engine: return sqlalchemy engine
    """
    sqlalchemy_db_url = f"{db_url}://{user}:{password}@{host}:{port}/{db_name}"
    return create_engine(sqlalchemy_db_url, echo=False)



Base = declarative_base()

engine = create_db_engine(
    db_url = 'postgresql+psycopg2',
    db_name = 'bruvs_ningloo',
    user = 'postgres',
    password = 'postgres',
    host = '127.0.0.1',
    port = '5432',
)

SessionLocal = sessionmaker()
SessionLocal.configure(
    autocommit=False,
    autoflush=False,
    binds={
        Base: engine,
    },
)


