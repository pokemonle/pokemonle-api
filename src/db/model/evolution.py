from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from db.model.base import Base


class EvolutionChain(Base):
    __tablename__ = 'evolution_chains'

    # id,identifier
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    baby_trigger_item_id = Column(Integer, ForeignKey("items.id"), nullable=True)

class EvolutionTrigger(Base):
    __tablename__ = 'evolution_triggers'

    # id,identifier
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    identifier: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

class EvolutionTriggerProse(Base):
    __tablename__ = 'evolution_trigger_prose'

    # evolution_trigger_id,local_language_id,name
    evolution_trigger_id: Mapped[int] = mapped_column(Integer, ForeignKey("evolution_triggers.id"), primary_key=True)
    local_language_id: Mapped[int] = mapped_column(Integer, ForeignKey("languages.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)