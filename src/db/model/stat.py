from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from .base import Base

class Stat(Base):
    __tablename__ = 'stats'

    # id,damage_class_id,identifier,is_battle_only,game_index
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    damage_class_id: Mapped[int] = mapped_column(Integer, ForeignKey('move_damage_classes.id'), nullable=True)
    identifier: Mapped[str] = mapped_column(String(50))
    is_battle_only = Column(Boolean, nullable=False)
    game_index = Column(Integer)

class StatName(Base):
    __tablename__ = 'stat_names'

    # stat_id,local_language_id,name
    stat_id: Mapped[int] = mapped_column(Integer, ForeignKey('stats.id'), primary_key=True)
    local_language_id: Mapped[int] = mapped_column(Integer, ForeignKey('languages.id'), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    def to_dict(self):
        return {
            "stat_id": self.stat_id,
            "local_language_id": self.local_language_id,
            "name": self.name
        }