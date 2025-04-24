from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from db.model.base import Base
from typing import List

class Type(Base):
    __tablename__ = 'types'

    # id,identifier,generation_id,damage_class_id
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    identifier: String = Column(String(50), nullable=False, unique=True)
    generation_id: Mapped[int] = mapped_column(Integer, ForeignKey('generations.id'), nullable=False)
    damage_class_id = Column(Integer, ForeignKey('move_damage_classes.id'))

    names: Mapped[List["TypeName"]] = relationship(back_populates="_type")

class TypeName(Base):
    __tablename__ = "type_names"

    # type_id,local_language_id,name

    type_id: Mapped[int] = mapped_column(Integer,ForeignKey("types.id"), primary_key=True)
    local_language_id: Mapped[int] = mapped_column(Integer,ForeignKey("languages.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    _type: Mapped["Type"] = relationship("Type", back_populates="names")
