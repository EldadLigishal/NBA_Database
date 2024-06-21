from pydantic import BaseModel

class TeamBase(BaseModel):
    conference: str
    division: str
    city: str
    name: str
    full_name: str
    abbreviation: str

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id : int
    class Config:
        orm_mode = True


class PlayerBase(BaseModel):
    first_name : str
    last_name : str
    position : str
    height : str
    weight : int
    jersey_number : int
    college : str
    country : str
    draft_year : int
    draft_pick : int
    team_id : int


class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    id: int
    class Config:
        orm_mode = True