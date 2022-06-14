from fastapi import FastAPI, Response
from api.decompose_roman import analyse_roman
from api.generate_kg import generate_kg

app = FastAPI()


@app.get("/")
async def root():
    return {"error": "No chord given"}


@app.get("/roman-chord-ontology/{roman_chord}")
async def say_hello(roman_chord: str) -> dict:
    decomposed_roman = analyse_roman(roman_chord)
    return Response(generate_kg(decomposed_roman))
