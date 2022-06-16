from fastapi import FastAPI, Response, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from rdflib import Graph

from api.decompose_roman import analyse_roman
from api.generate_kg import generate_kg
from api.validation import DecomposedChordModel

app = FastAPI()


@app.get("/")
async def root():
    raise HTTPException(status_code=404, detail="Not a valid roman numeral chord")


@app.get("/{roman_chord}", response_model=DecomposedChordModel)
async def root(roman_chord: str = Query(default=...,
                                        title="Roman Chord",
                                        description="A valid Music21 roman-numeral Chord")):
    try:
        decomposed_roman = analyse_roman(roman_chord)
        decomposed_roman_validated = jsonable_encoder(DecomposedChordModel(roman_chord=decomposed_roman))
    except ValidationError:
        raise HTTPException(status_code=404, detail="Unexpected decomposition chord output")
    except ValueError:
        raise HTTPException(status_code=404, detail="Not a valid roman numeral chord")
    return JSONResponse(decomposed_roman_validated)


@app.get("/roman-chord-ontology/{roman_chord}")
async def return_kg(roman_chord: str = Query(default=...,
                                             title="Roman Chord",
                                             description="A valid Music21 roman-numeral Chord: Validation Error")
                    ) -> Graph:
    try:
        decomposed_roman = analyse_roman(roman_chord)
        decomposed_roman_validated = DecomposedChordModel(roman_chord=decomposed_roman)
        decomposed_roman_validated = decomposed_roman_validated.roman_chord
    except ValidationError:
        raise HTTPException(status_code=404, detail="Unexpected decomposition chord output: Validation Error")
    if decomposed_roman_validated:
        try:
            kg = generate_kg(decomposed_roman_validated)
        except ValueError:
            raise HTTPException(status_code=404, detail="RDF conversion error")
    return Response(kg)
