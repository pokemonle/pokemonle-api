from typing import Annotated
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db.database import get_db
from db.model import Pokemon, PokemonSpecies, PokemonSpeciesName, PokemonStat, StatName

router = APIRouter(prefix="/pokemon", tags=["pokemon"])


@router.get('')
def list_pokemons(language: int = Query(12, alias='lang', ge=1, le=12), db: Session = Depends(get_db)):
    """ List pokemons with basic info"""
    data = (
        db.query(Pokemon, PokemonSpeciesName.name)
        .join(PokemonSpecies, Pokemon.species_id == PokemonSpecies.id)
        .join(PokemonSpeciesName, PokemonSpecies.id == PokemonSpeciesName.pokemon_species_id)
        .filter(PokemonSpeciesName.local_language_id == language)
        .all()
    )
    return JSONResponse(content=[{**p.to_dict(), 'name': name} for p, name in data])


@router.get('/name')
def list_pokemon_local_names(
        lang: Annotated[int, Query(ge=1, le=12)] = 12,
        search: Annotated[str | None, Query()] = None,
        limit :Annotated[int, Query(ge=1)] = 50,
        db: Session = Depends(get_db)
):
    """ List pokemon local names only."""
    query = db.query(PokemonSpeciesName).filter(PokemonSpeciesName.local_language_id == lang)
    if search:
        query = query.filter(PokemonSpeciesName.name.like(f"%{search}%"))
    data = [row.to_dict() for row in query.limit(limit).all()]
    return JSONResponse(content=data)


@router.get('/{pokemon_id}')
def get_pokemon_by_id(
        pokemon_id: int,
        language: int = Query(12, alias='lang', ge=1, le=12),
        db: Session = Depends(get_db)
):
    data = (
        db.query(Pokemon, PokemonSpeciesName.name)
        .join(PokemonSpecies, Pokemon.species_id == PokemonSpecies.id)
        .join(PokemonSpeciesName, PokemonSpecies.id == PokemonSpeciesName.pokemon_species_id)
        .filter(Pokemon.id == pokemon_id)
        .filter(PokemonSpeciesName.local_language_id == language)
        .first()
    )
    if data:
        p, name = data
        return JSONResponse(content={**p.to_dict(), 'name': name})
    else:
        return JSONResponse(content={"error": "Pokemon not found"}, status_code=404)


@router.get('/{pokemon_id}/stats')
def get_pokemon_stats(
        pokemon_id: int, language: int = Query(12, alias='lang', ge=1, le=12),
        db: Session = Depends(get_db)):
    data = (
        db.query(PokemonStat.base_stat, StatName.name)
        .join(StatName, PokemonStat.stat_id == StatName.stat_id)
        .filter(PokemonStat.pokemon_id == pokemon_id)
        .filter(StatName.local_language_id == language)
        .all()
    )

    if data:
        return JSONResponse(content={
            "sum": sum([base_stat for base_stat, _ in data]),
            "detail": [{'name': name, 'base_stat': base_stat} for base_stat, name in data]
        })
    else:
        return JSONResponse(content={"error": "Pokemon not found"}, status_code=404)
