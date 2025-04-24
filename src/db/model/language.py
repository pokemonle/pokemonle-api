from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from db.model.base import Base
from typing import List

class Language(Base):
    __tablename__ = 'languages'

    # id,iso639,iso3166,identifier,official,order

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    iso639 = Column(String(10), nullable=False)
    iso3166 = Column(String(10), nullable=False)
    identifier = Column(String(50), nullable=False)
    official = Column(Boolean, nullable=False)
    order = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "iso639": self.iso639,
            "iso3166": self.iso3166,
            "identifier": self.identifier,
            "official": self.official,
            "order": self.order
        }

class LanguageName(Base):
    __tablename__ = "language_names"

    # language_id,local_language_id,name
    language_id = Column(Integer, ForeignKey('languages.id'), primary_key=True)
    local_language_id = Column(Integer, ForeignKey('languages.id'), primary_key=True)
    name = Column(String(50), nullable=False)

    def to_dict(self):
        return {
            "language_id": self.language_id,
            "local_language_id": self.local_language_id,
            "name": self.name
        }

