from fastapi import FastAPI
from api.decompose_roman import analyse_roman

app = FastAPI()


@app.get("/")
async def root():
    return {"error": "No chord given"}


@app.get("/roman-chord-ontology/{roman_chord}")
async def say_hello(roman_chord: str) -> dict:
    return analyse_roman(roman_chord)
