from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from db.database import DBSession
from db.model import Version,VersionName

router = APIRouter(prefix="/version", tags=["version"])

@router.get('')
def index(language: int = Query(12, alias='lang', ge=1, le=12)):
    db = DBSession()
    data = (
        db.query(Version, VersionName.name)
        .join(VersionName, Version.id == VersionName.version_id)
        .filter(VersionName.local_language_id == language)
        .all()
    )
    return JSONResponse(content=[{**g.to_dict(), 'name': name} for g, name in data])

@router.get("/{version_id}")
def get(version_id: int, language: int = Query(12, alias='lang', ge=1, le=12)):
    db = DBSession()
    data = (
        db.query(Version, VersionName.name)
        .join(VersionName, Version.id == VersionName.version_id)
        .filter(VersionName.local_language_id == language)
        .filter(Version.id == version_id)
        .first()
    )
    if not data:
        return JSONResponse(status_code=404, content={"message": "Version not found"})
    return JSONResponse(content={**data[0].to_dict(), 'name': data[1]})