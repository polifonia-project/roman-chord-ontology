from fastapi import FastAPI, Response, HTTPException, Query

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from rdflib import Graph

from api.decompose_roman import analyse_roman
from api.generate_kg import generate_kg, DecomposedChordModel

app = FastAPI()


@app.get("/")
async def root():
    raise HTTPException(status_code=404, detail="Not a valid roman numeral chord")


@app.get("/{roman_chord}", response_model=DecomposedChordModel)
async def root(roman_chord: str = Query(default=...,
                                        title="Roman Chord",
                                        description="A valid Music21 roman-numeral Chord")):
    try:
        decomposed_roman = jsonable_encoder(analyse_roman(roman_chord))
    except ValueError:
        raise HTTPException(status_code=404, detail="Not a valid roman numeral chord")
    return JSONResponse(decomposed_roman)


@app.get("/roman-chord-ontology/{roman_chord}")
async def return_kg(roman_chord: str = Query(default=...,
                                             title="Roman Chord",
                                             description="A valid Music21 roman-numeral Chord")
                    ) -> Graph:
    decomposed_roman = analyse_roman(roman_chord)
    if decomposed_roman:
        try:
            kg = generate_kg(decomposed_roman)
        except ValueError:
            raise HTTPException(status_code=404, detail="RDF conversion error")
    return Response(kg)
