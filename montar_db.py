from sqlalchemy import create_engine, inspect
from src.Settings import Settings
from src.passaabolaapi.database.tables_database import Base

engine = create_engine(Settings().DATABASE_URL)


def listar_tabelas():
    inspector = inspect(engine)
    tabelas = inspector.get_table_names()
    return tabelas


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print(listar_tabelas())
