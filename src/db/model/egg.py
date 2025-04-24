from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from db.model.base import Base

class EggGroup(Base):
    __tablename__ = 'egg_groups'

    # id,identifier
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    identifier: Mapped[str] = mapped_column(String(50), nullable=False)

class EggGroupProse(Base):
    __tablename__ = 'egg_group_prose'

    # egg_group_id,local_language_id,name
    egg_group_id: Mapped[int] = mapped_column(Integer, ForeignKey('egg_groups.id'), primary_key=True)
    local_language_id: Mapped[int] = mapped_column(Integer, ForeignKey('languages.id'), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)