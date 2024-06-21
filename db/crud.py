from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db import entities, schemas

# Team queries
def get_team(db: Session, team_id: int):
    return db.query(entities.Team).filter(entities.Team.id == team_id).first()

def get_team_by_name(db: Session, name: str):
    return db.query(entities.Team).filter(entities.Team.name == name).first()

def get_team_by_abbreviation(db: Session, abbv: str):
    return db.query(entities.Team).filter(entities.Team.abbreviation == abbv).first()

def get_all_teams(db: Session):
    return db.query(entities.Team).order_by(entities.Team.id).all()

def add_team(db: Session, team: schemas.TeamCreate):
    # Check if the team already exists
    db_team = get_team_by_name(db, name=team.name)
    if db_team:
        raise HTTPException(status_code=400, detail="Team already registered")

    new_id = db.query(func.count(entities.Team.id)).scalar() + 1
    while get_team(db, new_id):
        new_id += 1
    db_team = entities.Team(id=new_id,
                            conference=team.conference,
                            division = team.division,
                            city=team.city,
                            name=team.name,
                            full_name=team.full_name,
                            abbreviation=team.abbreviation)

    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def update_city(db: Session, team_id: int, new_city : str):
    db_team = db.query(entities.Team).filter(entities.Team.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    db_team.city = new_city
    db_team.full_name = f"{new_city} {db_team.name}"
    db.commit()
    db.refresh(db_team)
    return db_team


# Player queries
def get_player(db: Session, player_id: int):
    return db.query(entities.Player).filter(entities.Player.id == player_id).first()

def get_player_by_name(db: Session, last_name: str):
    return db.query(entities.Player).filter(entities.Player.last_name == last_name).all()

def get_all_players(db: Session):
    return db.query(entities.Player).all()

def add_player(db: Session, player: schemas.PlayerCreate):
    new_id = db.query(func.count(entities.Player.id)).scalar() + 1

    db_player = entities.Player(id=new_id,
                                first_name = player.first_name,
                                last_name = player.last_name,
                                position= player.position,
                                height= player.height,
                                weight= player.weight,
                                jersey_number = player.jersey_number,
                                college= player.college,
                                country= player.country,
                                draft_year= player.draft_year,
                                draft_pick= player.draft_pick,
                                team_id= player.team_id)

    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player



def get_player_team(db, player_id):
    player = db.query(entities.Player).filter(entities.Player.id == player_id).first()
    team = db.query(entities.Team).filter(entities.Team.id == player.team_id).first()
    return team


def delete_team(db, team_id):
    db_team = db.query(entities.Team).filter(entities.Team.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    db.delete(db_team)
    db.commit()
    return