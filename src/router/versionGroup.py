from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from db.database import DBSession
from db.model import VersionGroup

router = APIRouter(prefix="/version-group", tags=["version"])


@router.get('')
def index():
    db = DBSession()
    data = db.query(VersionGroup).all()
    return JSONResponse(content=[v.to_dict() for v in data])

@router.get("/{version_group_id}")
def get(version_group_id: int):
    db = DBSession()
    data = db.query(VersionGroup).filter(VersionGroup.id == version_group_id).first()
    if not data:
        return JSONResponse(status_code=404, content={"message": "Version group not found"})
    return JSONResponse(content=data.to_dict())