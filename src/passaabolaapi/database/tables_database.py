from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import Session, DeclarativeBase
from src.Settings import Settings
import cuid


engine = create_engine(Settings().DATABASE_URL)
session = Session(engine)

def get_session():
    with Session(engine) as session:
        yield session

class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)

class JogadoraDB(Base):
    __tablename__ = "jogadoras"
    nome = Column(String, unique=True, nullable=False)
    id_time = Column(Integer, ForeignKey("times.id"), nullable=False)

class JogoDB(Base):
    __tablename__ = "jogos"
    time_1_id = Column(Integer, ForeignKey("times.id"), nullable=False)
    time_2_id = Column(Integer, ForeignKey("times.id"), nullable=False)
    gols_1 = Column(Integer, default=0, nullable=False)
    gols_2 = Column(Integer, default=0, nullable=False)

class TimeDB(Base):
    __tablename__ = "times"
    nome = Column(String, unique=True, nullable=False)
    gols = Column(Integer, nullable=False, default=0)
