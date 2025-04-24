from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from db.model.base import Base
from typing import List

class Generation(Base):
    __tablename__ = 'generations'

    # id,main_region_id,identifier
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    main_region_id = Column(Integer, nullable=False)
    identifier = Column(String(50), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'main_region_id': self.main_region_id,
            'identifier': self.identifier,
        }

class GenerationName(Base):
    __tablename__ = 'generation_names'

    # generation_id,local_language_id,name
    generation_id: Mapped[int] = mapped_column(Integer, ForeignKey('generations.id'), primary_key=True)
    local_language_id: Mapped[int] = mapped_column(Integer, ForeignKey('languages.id'), primary_key=True)
    name = mapped_column(String(50), nullable=False)

