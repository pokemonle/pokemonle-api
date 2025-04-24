import random
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from db.database import DBSession
from db.model import PokemonSpecies, PokemonSpeciesName
from utils.gen import decode_gen
from utils.compare import compare_pokemon

router = APIRouter(prefix="/game", tags=["game"])


@router.get('/init')
def init(
        encode: Annotated[int, Query(alias="gen")],
        difficulty=0,
):
    if difficulty == 0:
        db = DBSession()
        gens = decode_gen(encode)
        pokemon_list = (
            db.query(PokemonSpecies)
            .filter(PokemonSpecies.generation_id.in_(gens))
            .all()
        )
        # get random pokemon
        pokemon = random.choice(pokemon_list)

        return pokemon.id

    return 0


@router.get('/guess')
def check_answer(
        answer: int,
        guess: str,
        lang: Annotated[int, Query(ge=1, le=12)] = 12,
):
    db = DBSession()
    # find pokemon by guess name
    guess_pokemon_name = (
        db.query(PokemonSpeciesName)
        .filter(PokemonSpeciesName.local_language_id == lang)
        .filter(PokemonSpeciesName.name == guess)
        .first()
    )

    if guess_pokemon_name is None:
        return JSONResponse(content={"error": f"Guess Pokemon {guess} not found"}, status_code=404)

    (guess_pokemon, answer_pokemon) = (
        db.query(PokemonSpecies)
        .filter(PokemonSpecies.id == guess_pokemon_name.pokemon_species_id)
        .first(),
        db.query(PokemonSpecies)
        .filter(PokemonSpecies.id == answer)
        .first(),
    )

    if guess_pokemon is None or answer_pokemon is None:
        return JSONResponse(content={
            "error": "Pokemon not found",
            "guess": guess_pokemon_name.pokemon_species_id,
            "answer": answer,
        },
            status_code=404)

    return {
        **compare_pokemon(db,guess_pokemon, answer_pokemon, lang),
        "name": guess,
        "index": guess_pokemon.id,
    }


