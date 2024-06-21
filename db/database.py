import json

import requests
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import ProgrammingError

from app.db import entities


username = "postgres"
password = "root"
host = "localhost"
port = "5432"
database_name = 'nba_db'
DATABASE_URL = f'postgresql://{username}:{password}@{host}:{port}/{database_name}'
# Create an engine to the PostgreSQL server
try:
    engine = create_engine(DATABASE_URL)
    print("Database connection was successful")
except ProgrammingError as e:
    print(e)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



api_url = 'https://api.balldontlie.io/v1/players?per_page=100'
api_key = 'b71b4b8a-c6cd-4c07-bb8d-d78818f71992'

# Create headers including the API key
headers = {
    'Authorization': f'{api_key}'
}

# Make the GET request to the API
response = requests.get(api_url, headers=headers)


# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response to a Python dictionary
    data = response.json()

else:
    # Handle errors
    print(f"Failed to fetch data: {response.status_code}")
    print(response.text)



"""
TODO: Move all the methods below to crud.py
"""
def add_team(team):
    db: Session = SessionLocal()
    try:
        db_team = entities.Team(id = team['id'],
                                conference = team['conference'],
                                division = team['division'],
                                city = team['city'],
                                name = team['name'],
                                full_name = f"{team['city']} {team['name']}",
                                abbreviation = team['abbreviation'])

        db.add(db_team)
        db.commit()
        db.refresh(db_team)
        # print(f"Added Team: {db_team.id}, {db_team.name}")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()


def add_player(player):
    db: Session = SessionLocal()
    try:
        db_player = entities.Player(id = player['id'],
                                  first_name = player['first_name'],
                                  last_name = player['last_name'],
                                  position = player['position'],
                                  height = player['height'],
                                  weight = player['weight'],
                                  jersey_number = player['jersey_number'],
                                  college = player['college'],
                                  country = player['country'],
                                  draft_year = player['draft_year'],
                                  draft_pick = player['draft_number'],
                                  team_id = player['team']['id'])

        db.add(db_player)
        db.commit()
        db.refresh(db_player)
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()


def save_json():
    team_api = 'https://api.balldontlie.io/v1/teams?per_page=30'
    teams_api = requests.get(team_api, headers=headers).json()

    # Write JSON object to a file
    with open("teams.json", 'w') as file:
        json.dump(teams_api, file, indent=4)  # indent=4 for pretty printing


def api_fetch_teams():
    team_api = 'https://api.balldontlie.io/v1/teams?per_page=30'
    teams_api = requests.get(team_api, headers=headers).json()
    save_json()
    teams_db = []
    for i in range(30):
        teams_db.append(teams_api['data'][i])
        add_team(teams_db[-1])
    print(f"Added {len(teams_db)} teams to Teams table")
    return teams_db

def api_fetch_players():
    page = 0
    players_db = []
    while page < 500:
        if page == 0:
            url = f'https://api.balldontlie.io/v1/players?cursor={page}&per_page=100'
            response = requests.get(url, headers=headers).json()
        for i in range(100):
            players_db.append(response['data'][i])
            add_player(players_db[-1])
            # only 493 active players
            if len(players_db) == 493:
                break
        page += 100
        url = f'https://api.balldontlie.io/v1/players?cursor={page}&per_page=100'

        response = requests.get(url, headers=headers).json()

    # print(players_db[-1])
    print(f"Added {len(players_db)} players to Players table")
    return players_db

