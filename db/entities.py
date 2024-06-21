from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import Relationship, declarative_base
# from .database import Base

Base = declarative_base()
class Team(Base):
    __tablename__ = "Teams"

    id = Column(Integer(), primary_key=True)
    conference = Column(String(4), nullable=False)
    division = Column(String(), nullable=False)
    city = Column(String(), nullable=False)
    name = Column(String(), nullable=False)
    full_name = Column(String(), nullable=False)
    abbreviation = Column(String(3), nullable=False)



class Player(Base):
    __tablename__ = "Players"

    id = Column(Integer(), primary_key=True)
    first_name = Column(String(), nullable=False)
    last_name = Column(String(), nullable=False)
    position = Column(String(), nullable=False)
    height = Column(String())
    weight = Column(Integer())
    jersey_number = Column(Integer())
    college = Column(String())
    country = Column(String())
    draft_year = Column(Integer())
    draft_pick = Column(Integer())
    # if we delete Teams, this one will be deleted too
    team_id = Column(Integer(), ForeignKey("Teams.id", ondelete="CASCADE"), nullable=False)
    team = Relationship("Team")