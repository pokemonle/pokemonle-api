from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from db.model.base import Base

class VersionGroup(Base):
    __tablename__ = 'version_groups'

    # id,identifier,generation_id,order
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    identifier = Column(String(50), nullable=False, unique=True)
    generation_id: Mapped[int] = mapped_column(Integer, ForeignKey('generations.id'), nullable=False)
    order: Mapped[int] = mapped_column(Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'identifier': self.identifier,
            'generation_id': self.generation_id,
            'order': self.order
        }

class Version(Base):
    __tablename__ = 'versions'

    # id,version_group_id,identifier
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    version_group_id: Mapped[int] = mapped_column(Integer, ForeignKey('version_groups.id'), nullable=False)
    identifier = Column(String(50), nullable=False, unique=True)

    def to_dict(self):
        return {
            'id': self.id,
            'version_group_id': self.version_group_id,
            'identifier': self.identifier
        }

    # relationships
    # version_group = relationship("VersionGroup", back_populates="versions")

class VersionName(Base):
    __tablename__ = 'version_names'

    # version_id,local_language_id,name
    version_id: Mapped[int] = mapped_column(Integer, ForeignKey('versions.id'), primary_key=True)
    local_language_id: Mapped[int] = mapped_column(Integer, ForeignKey('languages.id'), primary_key=True)
    name = Column(String(50), nullable=False)