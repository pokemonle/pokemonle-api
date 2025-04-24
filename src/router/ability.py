from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from db.database import DBSession
from db.model import Ability, AbilityName, AbilityFlavorText

router = APIRouter(prefix="/ability", tags=["ability"])


@router.get('')
def index(language: int = Query(12, alias='lang', ge=1, le=12)):
    db = DBSession()
    data = (
        db.query(Ability, AbilityName.name)
        .join(AbilityName, Ability.id == AbilityName.ability_id)
        .filter(AbilityName.local_language_id == language)
        .all()
    )
    return JSONResponse(content=[{**g.to_dict(), 'name': name} for g, name in data])


@router.get('/{ability_id}')
def get(ability_id: int, language: int = Query(12, alias='lang', ge=1, le=12)):
    db = DBSession()
    data = (
        db.query(Ability, AbilityName.name)
        .join(AbilityName, Ability.id == AbilityName.ability_id)
        .filter(AbilityName.local_language_id == language)
        .filter(Ability.id == ability_id)
        .first()
    )
    if not data:
        return JSONResponse(status_code=404, content={"message": "Ability not found"})
    return JSONResponse(content={**data[0].to_dict(), 'name': data[1]})
