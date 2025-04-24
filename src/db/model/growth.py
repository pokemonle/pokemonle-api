from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from db.model.base import Base

class GrowthRate(Base):
    __tablename__ = 'growth_rates'

    # id,identifier
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    identifier: Mapped[str] = mapped_column(String(50), nullable=False)
    formula = Column(String(500), nullable=False)

class GrowthRateProse(Base):
    __tablename__ = 'growth_rate_prose'

    # growth_rate_id,local_language_id,name
    growth_rate_id: Mapped[int] = mapped_column(Integer, ForeignKey('growth_rates.id'), primary_key=True)
    local_language_id: Mapped[int] = mapped_column(Integer, ForeignKey('languages.id'), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)