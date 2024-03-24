from sqlalchemy import Column, Integer, String, PickleType
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    username = Column(String, primary_key=True)
    user_level = Column(String)
    password = Column(String)


class Agent(Base):
    __tablename__ = 'agent'
    agent_id = Column(Integer, primary_key=True, autoincrement=True)
    agent_name = Column(String)
    agent_type = Column(String)
    prompt = Column(PickleType)
    username_belongs_to = Column(String)

