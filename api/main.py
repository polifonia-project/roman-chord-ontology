"""
File containing all the scripts of the FastAPI APIs
"""

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
    """
    Base API root
    :raise: HTTPException
    """
    raise HTTPException(status_code=404, detail="Not a valid roman numeral chord")


@app.get("/{roman_chord}", response_model=DecomposedChordModel)
async def root(roman_chord: str = Query(default=...,
                                        title="Roman Chord",
                                        description="A valid Music21 roman-numeral Chord")):
    """
    Base API root + a roman chord
    :param roman_chord: str
        A valid Roman Numeral Chord, i.e. a Roman Numeral Chord
        interpretable by the music21.roman library/module
    :return: JSONResponse
        A JSONResponse output containing the validated constituting elements of a chord
    :raise: ValidationError
        If the output of the analysis is not consistent with the model, it returns a
        ValidationError
    :raise: ValueError
        If the input is not a valid music21.roman chord, it returns a ValueError
    """
    try:
        decomposed_roman = analyse_roman(roman_chord)
        decomposed_roman_validated = jsonable_encoder(DecomposedChordModel(roman_chord=decomposed_roman))
    except ValidationError as validation_error:
        raise HTTPException(status_code=404, detail=f'Unexpected decomposition chord output: {validation_error}')
    except ValueError:
        raise HTTPException(status_code=404, detail='Not a valid roman numeral chord')
    return JSONResponse(decomposed_roman_validated)


@app.get("/roman-chord-ontology/{roman_chord}")
async def return_kg(roman_chord: str = Query(default=...,
                                             title='Roman Chord',
                                             description='A valid Music21 roman-numeral Chord')
                    ) -> Graph:
    """
    Base API root + roman-chord-ontology + a roman chord
    :param roman_chord: str
        A valid Roman Numeral Chord, i.e. a Roman Numeral Chord
        interpretable by the music21.roman library/module
    :return: Response
        A Response containing a serialised RDF Knowledge Graph of the input chord
    :raise: ValidationError
        If the output of the analysis is not consistent with the model, it returns a
        ValidationError
    :raise: ValueError
        If the input is not a valid music21.roman chord, it returns a ValueError
    """
    try:
        decomposed_roman = analyse_roman(roman_chord)
        decomposed_roman_validated = DecomposedChordModel(roman_chord=decomposed_roman)
        decomposed_roman_validated = decomposed_roman_validated.roman_chord
    except ValidationError as validation_error:
        raise HTTPException(status_code=404, detail=f'Unexpected decomposition chord output: {validation_error}')
    if decomposed_roman_validated:
        try:
            kg = generate_kg(decomposed_roman_validated)
        except ValueError:
            raise HTTPException(status_code=404, detail="RDF conversion error")
    return Response(kg)
