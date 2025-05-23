from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db.database import get_db
from db.model import Generation, GenerationName

router = APIRouter(prefix="/gen", tags=["generation"])


@router.get('')
def index(language: int = Query(12, alias='lang', ge=1, le=12), db: Session = Depends(get_db)):
    data = (
        db.query(Generation, GenerationName.name)
        .join(GenerationName, Generation.id == GenerationName.generation_id)
        .filter(GenerationName.local_language_id == language)
        .all()
    )
    return JSONResponse(content=[{**g.to_dict(), 'name': name} for g, name in data])


@router.get("/{generation_id}")
def get(generation_id: int, language: int = Query(12, alias='lang', ge=1, le=12), db: Session = Depends(get_db)):
    data = (
        db.query(Generation, GenerationName.name)
        .join(GenerationName, Generation.id == GenerationName.generation_id)
        .filter(GenerationName.local_language_id == language)
        .filter(Generation.id == generation_id)
        .first()
    )
    if not data:
        return JSONResponse(status_code=404, content={"message": "Generation not found"})
    return JSONResponse(content={**data[0].to_dict(), 'name': data[1]})
