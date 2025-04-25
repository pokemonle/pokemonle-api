from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db.database import get_db
from db.model import Language, LanguageName

router = APIRouter(prefix="/lang", tags=["language"])


@router.get('')
def list_language(
        language: int = Query(12, alias='lang', ge=1, le=12),
        db: Session = Depends(get_db)):
    data = (
        db.query(Language, LanguageName.name)
        .join(LanguageName, Language.id == LanguageName.language_id)
        .filter(LanguageName.local_language_id == language)
        .all()
    )
    return [{**g.to_dict(), 'name': name} for g, name in data]
    # return JSONResponse(content=[{**g.to_dict(), 'name': name} for g, name in data])


@router.get("/{language_id}")
def get_language_by_id(language_id: int, language: int = Query(12, alias='lang', ge=1, le=12),
                       db: Session = Depends(get_db)):
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
