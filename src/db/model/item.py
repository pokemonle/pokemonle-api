from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from db.model.base import Base

class ItemPocket(Base):
    __tablename__ = 'item_pockets'

    # id,identifier
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    identifier: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

class ItemPocketName(Base):
    __tablename__ = 'item_pocket_names'

    # item_pocket_id,local_language_id,name
    item_pocket_id: Mapped[int] = mapped_column(Integer, ForeignKey("item_pockets.id"), primary_key=True)
    local_language_id: Mapped[int] = mapped_column(Integer, ForeignKey("languages.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

class ItemCategory(Base):
    __tablename__ = 'item_categories'

    # id,pocket_id,identifier
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pocket_id: Mapped[int] = mapped_column(Integer, ForeignKey("item_pockets.id"), nullable=False)
    identifier: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

class Item(Base):
    __tablename__ = 'items'

    # id,identifier,category_id,cost,fling_power,fling_effect_id
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    identifier: Mapped[str] = mapped_column(String(50), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("item_categories.id"), nullable=False)
    cost = Column(Integer, nullable=False)
    fling_power = Column(Integer)
    fling_effect_id = Column(Integer, ForeignKey("item_fling_effects.id"), nullable=True)

class ItemName(Base):
    __tablename__ = 'item_names'

    # item_id,local_language_id,name
    item_id: Mapped[int] = mapped_column(Integer, ForeignKey("items.id"), primary_key=True)
    local_language_id: Mapped[int] = mapped_column(Integer, ForeignKey("languages.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

class ItemFlingEffect(Base):
    __tablename__ = 'item_fling_effects'

    # id,identifier
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    identifier: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

class ItemFlingEffectProse(Base):
    __tablename__ = 'item_fling_effect_prose'

    # item_fling_effect_id,local_language_id,name
    item_fling_effect_id: Mapped[int] = mapped_column(Integer, ForeignKey("item_fling_effects.id"), primary_key=True)
    local_language_id: Mapped[int] = mapped_column(Integer, ForeignKey("languages.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)