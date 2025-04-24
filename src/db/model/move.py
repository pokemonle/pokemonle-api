from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from db.model.base import Base
from typing import List

class MoveDamageClass(Base):
    __tablename__ = 'move_damage_classes'

    # id,identifier
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    identifier: Mapped[str] = mapped_column(String(50), nullable=False)

    # relationships
    # moves: Mapped[List["Move"]] = relationship(back_populates="_move_damage_class")

class MoveDamageClassProse(Base):
    __tablename__ = "move_damage_class_prose"

    # move_damage_class_id,local_language_id,name,description
    move_damage_class_id: Mapped[int] = mapped_column(Integer,ForeignKey("move_damage_classes.id"), primary_key=True)
    local_language_id: Mapped[int] = mapped_column(Integer,ForeignKey("languages.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
