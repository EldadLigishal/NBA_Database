from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from db import entities, schemas
from db import database, crud

entities.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def init():
    global teams_db, players_db
    teams_db = database.api_fetch_teams()
    players_db = database.api_fetch_players()



@app.get("/")
def home():
    return {"data": "Test"}

##########################  Teams endpoints   ###################################
@app.get("/api/teams/")
def fetch_teams(db: Session = Depends(database.get_db)):
    teams = crud.get_all_teams(db)
    return teams

@app.get("/api/teams/{team_id}")
def read_team_by_id(team_id : int, db: Session = Depends(database.get_db)):
    db_team = crud.get_team(db, team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team

@app.get("/api/teams/name/{name}")
def read_team_by_name(name : Optional[str] = None, db: Session = Depends(database.get_db)):
    db_team = crud.get_team_by_name(db, name)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team


@app.get("/api/teams/abbv/{abbv}")
def read_team_by_abbreviation(abbv : Optional[str] = None, db: Session = Depends(database.get_db)):
    db_team = crud.get_team_by_abbreviation(db, abbv)
    # db_team = db.query(entities.Team).filter(entities.Team.abbreviation == abbv).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team

@app.get("/api/teams/player/{player_id}", response_model=schemas.Team)
def read_team_by_player(player_id : int, db: Session = Depends(database.get_db)):
    return crud.get_player_team(db, player_id)

@app.post("/api/teams/", response_model=schemas.Team)
def create_team(team: schemas.TeamCreate, db: Session = Depends(database.get_db)):
    return crud.add_team(db=db, team=team)

@app.put("/api/teams/{team_id}")
def update_team_city(team_id: int, new_city: str, db: Session = Depends(database.get_db)):
    return crud.update_city(db, team_id, new_city)

@app.delete("/teams/{team_id}")
def delete_team(team_id: int, db: Session = Depends(database.get_db)):
    crud.delete_team(db, team_id)
    return

##########################  Players endpoints   ###################################
@app.get("/api/players/")
def fetch_players(db: Session = Depends(database.get_db)):
    players = crud.get_all_players(db)
    return players

@app.get("/api/players/{player_id}")
def read_player_by_id(player_id : int, db: Session = Depends(database.get_db)):
    db_player = crud.get_player(db, player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player


@app.get("/api/players/name/{last_name}")
def read_player_by_name(last_name : Optional[str] = None, db: Session = Depends(database.get_db)):
    db_players = crud.get_player_by_name(db, last_name)
    if not db_players:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_players


@app.post("/api/players/", response_model=schemas.Player)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(database.get_db)):
    return crud.add_player(db=db, player=player)





if __name__ == "__main__":
    import uvicorn
    init()
    uvicorn.run(app, host="127.0.0.1", port=8000)
