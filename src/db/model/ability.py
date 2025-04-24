from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,PrimaryKeyConstraint
from sqlalchemy.orm import relationship, mapped_column, Mapped
from db.model.base import Base

class Ability(Base):
    __tablename__ = 'abilities'

    # id,identifier,generation_id,is_main_series
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    identifier = Column(String(50), nullable=False, unique=True)
    generation_id: Mapped[int] = mapped_column(Integer, ForeignKey('generations.id'), nullable=False)
    is_main_series = Column(Boolean)

    def to_dict(self):
        return {
            'id': self.id,
            'identifier': self.identifier,
            'generation_id': self.generation_id,
            'is_main_series': self.is_main_series
        }

class AbilityFlavorText(Base):
    __tablename__ = 'ability_flavor_text'

    # ability_id,version_group_id,language_id,flavor_text
    ability_id: Mapped[int] = mapped_column(Integer, ForeignKey('abilities.id'))
    version_group_id: Mapped[int] = mapped_column(Integer, ForeignKey('version_groups.id'))
    language_id: Mapped[int] = mapped_column(Integer, ForeignKey('languages.id'))
    flavor_text = Column(String(255), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('ability_id', 'version_group_id', 'language_id'),
    )


class AbilityName(Base):
    __tablename__ = 'ability_names'

    # ability_id,local_language_id,name
    ability_id: Mapped[int] = mapped_column(Integer, ForeignKey('abilities.id'), primary_key=True)
    local_language_id: Mapped[int] = mapped_column(Integer, ForeignKey('languages.id'), primary_key=True)
    name = Column(String(50), nullable=False)

    def to_dict(self):
        return {
            'ability_id': self.ability_id,
            'local_language_id': self.local_language_id,
            'name': self.name
        }