from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from db.database import DBSession
from db.model import Language, LanguageName

router = APIRouter(prefix="/lang", tags=["lang"])


@router.get('')
def index(language: int = Query(12, alias='lang', ge=1, le=12)):
    db = DBSession()
    data = (
        db.query(Language, LanguageName.name)
        .join(LanguageName, Language.id == LanguageName.language_id)
        .filter(LanguageName.local_language_id == language)
        .all()
    )
    return JSONResponse(content=[{**g.to_dict(), 'name': name} for g, name in data])

@router.get("/{language_id}")
def get(language_id: int, language: int = Query(12, alias='lang', ge=1, le=12)):
    db = DBSession()
    data = (
        db.query(Language, LanguageName.name)
        .join(LanguageName, Language.id == LanguageName.language_id)
        .filter(LanguageName.local_language_id == language)
        .filter(Language.id == language_id)
        .first()
    )
    if not data:
        return JSONResponse(status_code=404, content={"message": "Language not found"})
    return JSONResponse(content={**data[0].to_dict(), 'name': data[1]})