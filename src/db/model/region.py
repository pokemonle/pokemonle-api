from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from db.model.base import Base

class Region(Base):
    __tablename__ = "regions"

    # id,identifier
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    identifier: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)

class RegionName(Base):
    __tablename__ = "region_names"

    # region_id,local_language_id,name
    region_id: Mapped[int] = mapped_column(Integer, ForeignKey("regions.id"), primary_key=True)
    local_language_id: Mapped[int] = mapped_column(Integer, ForeignKey("languages.id"), primary_key=True)
    name : Mapped[str] = mapped_column(String(30), nullable=False)