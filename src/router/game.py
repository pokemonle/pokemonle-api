import random
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db.database import get_db
from db.model import PokemonSpecies, PokemonSpeciesName
from utils.gen import decode_gen
from utils.compare import compare_pokemon

router = APIRouter(prefix="/game", tags=["game"])


@router.get('/init')
def init_game_answer(
        encode: Annotated[int, Query(alias="gen")],
        difficulty: int = 0,
        db: Session = Depends(get_db)
):
    """ Generate a random pokemon id for the game by difficulty and encode generation"""
    if difficulty == 0:
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
        guess: int,
        lang: Annotated[int, Query(ge=1, le=12)] = 12,
        db: Session = Depends(get_db)
):
    # find pokemon by guess name
    guess_pokemon_name = (
        db.query(PokemonSpeciesName)
        .filter(PokemonSpeciesName.local_language_id == lang)
        .filter(PokemonSpeciesName.pokemon_species_id == guess)
        .first()
    )

    if guess_pokemon_name is None:
        return JSONResponse(content={"error": f"Guess Pokemon ID {guess} not found"}, status_code=404)

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
        **compare_pokemon(db, guess_pokemon, answer_pokemon, lang),
        "identifier": guess_pokemon.identifier,
        "index": guess_pokemon.id,
    }


@router.get('/answer')
def get_answer(
        pokemon_id: Annotated[int, Query(alias="pokemon")],
        lang: Annotated[int, Query(ge=1, le=12)] = 12,
        db: Session = Depends(get_db)
):
    pokemon = (
        db.query(PokemonSpecies)
        .filter(PokemonSpecies.id == pokemon_id)
        .first()
    )

    name = (
        db.query(PokemonSpeciesName.name)
        .filter(PokemonSpeciesName.pokemon_species_id == pokemon_id)
        .filter(PokemonSpeciesName.local_language_id == lang)
        .first()
    )

    if pokemon is None:
        return JSONResponse(content={"error": f"Pokemon {pokemon_id} not found"}, status_code=404)

    if name is None:
        return JSONResponse(content={"error": f"Pokemon {pokemon_id} name not found"}, status_code=404)

    return {
        **compare_pokemon(db, pokemon, pokemon, lang),
        "name": name[0],
        "index": pokemon_id,
    }
