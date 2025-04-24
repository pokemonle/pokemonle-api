from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from db.model.base import Base

class Location(Base):
    __tablename__ = "locations"

    # id,region_id,identifier
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    region_id: Mapped[int] = mapped_column(Integer, ForeignKey("regions.id"), nullable=True)
    identifier: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)

class LocationName(Base):
    __tablename__ = "location_names"

    # location_id,local_language_id,name,subtitle
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey("locations.id"), primary_key=True)
    local_language_id: Mapped[int] = mapped_column(Integer, ForeignKey("languages.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    subtitle: Mapped[str] = mapped_column(String(100))