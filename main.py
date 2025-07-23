from fastapi import FastAPI, HTTPException
from models import Voting
import os
import json

app = FastAPI()
VOTINGS_DIR = "votings"
os.makedirs(VOTINGS_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Hello Mato"}

@app.post("/add-voting")
async def add_voting(voting: Voting):
    file_path = os.path.join(VOTINGS_DIR, f"{voting.id}.json")
    if os.path.exists(file_path):
        raise HTTPException(400, "Voting already exists.")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(voting.dict(), f, ensure_ascii=False, indent=2)
    return {"message": "Voting successfully added.", "id": voting.id}

@app.get("/get-voting/{id}", response_model=Voting)
async def get_voting(id: int):
    file_path = os.path.join(VOTINGS_DIR, f"{id}.json")
    if not os.path.exists(file_path):
        raise HTTPException(404, "Voting not found.")
    with open(file_path, "r", encoding="utf-8") as f:
        voting_data = json.load(f)
    return voting_data

@app.post("/switch-voting/{id}", response_model=Voting)
async def switch_voting(id: int):
    file_path = os.path.join(VOTINGS_DIR, f"{id}.json")
    if not os.path.exists(file_path):
        raise HTTPException(404, "Voting not found.")
    with open(file_path, "r", encoding="utf-8") as f:
        voting = Voting(**json.load(f))

    if voting.active:
        voting.active = False
    else:
        voting.active = True

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(voting.dict(), f, ensure_ascii=False, indent=2)

    return voting

@app.post("/vote/{id}")
async def vote(id: int, option: str):
    file_path = os.path.join(VOTINGS_DIR, f"{id}.json")
    if not os.path.exists(file_path):
        raise HTTPException(404, "Voting not found.")
    with open(file_path, "r", encoding="utf-8") as f:
        voting = Voting(**json.load(f))
    if not voting.active:
        raise HTTPException(403, "Voting is closed.")
    if option not in voting.options:
        raise HTTPException(400, "Invalid option.")

    voting.results.append(option)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(voting.dict(), f, ensure_ascii=False, indent=2)

    return {"message": "Vote successfully recorded."}

@app.get("/get-vote/{id}")
async def get_vote(id: int):
    file_path = os.path.join(VOTINGS_DIR, f"{id}.json")
    if not os.path.exists(file_path):
        raise HTTPException(404, "Voting not found.")
    with open(file_path, "r", encoding="utf-8") as f:
        voting = Voting(**json.load(f))
    return {"question": voting.question, "answers": voting.options}


@app.get("/status/{id}")
async def status(id: int):
    file_path = os.path.join(VOTINGS_DIR, f"{id}.json")
    if not os.path.exists(file_path):
        raise HTTPException(404, "Voting not found.")
    with open(file_path, "r", encoding="utf-8") as f:
        voting = Voting(**json.load(f))
    if voting.active:
        return {"active": voting.active}
    return {"active": voting.active, "results": voting.results}

