from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db.database import get_db
from db.model import VersionGroup

router = APIRouter(prefix="/version-group", tags=["version"])


@router.get('')
def list_version_groups(db: Session = Depends(get_db)):
    data = db.query(VersionGroup).all()
    return JSONResponse(content=[v.to_dict() for v in data])


@router.get("/{version_group_id}")
def get_version_group_by_id(version_group_id: int, db: Session = Depends(get_db)):
    data = db.query(VersionGroup).filter(VersionGroup.id == version_group_id).first()
    if not data:
        return JSONResponse(status_code=404, content={"message": "Version group not found"})
    return JSONResponse(content=data.to_dict())
