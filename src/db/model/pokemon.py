from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from db.model.base import Base


class PokemonColor(Base):
    __tablename__ = 'pokemon_colors'

    # id,identifier
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    identifier: Mapped[str] = mapped_column(String(50), nullable=False)


class PokemonColorName(Base):
    __tablename__ = 'pokemon_color_names'

    # pokemon_color_id,local_language_id,name
    pokemon_color_id: Mapped[int] = mapped_column(Integer, ForeignKey('pokemon_colors.id'), primary_key=True)
    local_language_id: Mapped[int] = mapped_column(Integer, ForeignKey('languages.id'), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)


class PokemonShape(Base):
    __tablename__ = 'pokemon_shapes'

    # id,identifier
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    identifier: Mapped[str] = mapped_column(String(50), nullable=False)


class PokemonHabitat(Base):
    __tablename__ = 'pokemon_habitats'

    # id,identifier
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    identifier: Mapped[str] = mapped_column(String(50), nullable=False)


class PokemonHabitatName(Base):
    __tablename__ = 'pokemon_habitat_names'

    # pokemon_habitat_id,local_language_id,name
    pokemon_habitat_id: Mapped[int] = mapped_column(Integer, ForeignKey('pokemon_habitats.id'), primary_key=True)
    local_language_id: Mapped[int] = mapped_column(Integer, ForeignKey('languages.id'), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)


class PokemonSpecies(Base):
    __tablename__ = 'pokemon_species'

    # id,identifier,generation_id,evolves_from_species_id,evolution_chain_id,color_id,shape_id,habitat_id,gender_rate,capture_rate,base_happiness,is_baby,hatch_counter,has_gender_differences,growth_rate_id,forms_switchable,is_legendary,is_mythical,order,conquest_order
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    identifier = Column(String(50), nullable=False)

    generation_id = Column(Integer, ForeignKey("generations.id"), nullable=False)
    evolves_from_species_id = Column(Integer, ForeignKey("pokemon_species.id"))
    evolution_chain_id = Column(Integer, ForeignKey("evolution_chains.id"))
    color_id = Column(Integer, ForeignKey("pokemon_colors.id"), nullable=False)
    shape_id = Column(Integer, ForeignKey("pokemon_shapes.id"), nullable=False)
    habitat_id = Column(Integer, ForeignKey("pokemon_habitats.id"))

    gender_rate = Column(Integer)
    capture_rate = Column(Integer)
    base_happiness = Column(Integer)
    is_baby = Column(Boolean, nullable=False)
    hatch_counter = Column(Integer, nullable=False)
    has_gender_differences = Column(Boolean, nullable=False)

    growth_rate_id = Column(Integer, ForeignKey("growth_rates.id"), nullable=False)
    forms_switchable = Column(Boolean, nullable=False)
    is_legendary = Column(Boolean, nullable=False)
    is_mythical = Column(Boolean, nullable=False)
    order = Column(Integer, nullable=False)
    conquest_order = Column(Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "identifier": self.identifier,
            "generation_id": self.generation_id,
            "evolves_from_species_id": self.evolves_from_species_id,
            "evolution_chain_id": self.evolution_chain_id,
            "color_id": self.color_id,
            "shape_id": self.shape_id,
            "habitat_id": self.habitat_id,
            "gender_rate": self.gender_rate,
            "capture_rate": self.capture_rate,
            "base_happiness": self.base_happiness,
            "is_baby": self.is_baby,
            "hatch_counter": self.hatch_counter,
            "has_gender_differences": self.has_gender_differences,
            "growth_rate_id": self.growth_rate_id,
            "forms_switchable": self.forms_switchable,
            "is_legendary": self.is_legendary,
            "is_mythical": self.is_mythical,
            "order": self.order,
            "conquest_order": self.conquest_order
        }


class PokemonSpeciesName(Base):
    __tablename__ = 'pokemon_species_names'

    # pokemon_species_id,local_language_id,name
    pokemon_species_id: Mapped[int] = mapped_column(Integer, ForeignKey('pokemon_species.id'), primary_key=True)
    local_language_id: Mapped[int] = mapped_column(Integer, ForeignKey('languages.id'), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    genus: Mapped[str] = mapped_column(String(50))

    def to_dict(self):
        return {
            "pokemon_species_id": self.pokemon_species_id,
            "local_language_id": self.local_language_id,
            "name": self.name,
            "genus": self.genus
        }


class Pokemon(Base):
    __tablename__ = 'pokemon'

    # id,identifier,species_id,height,weight,base_experience,order,is_default
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    identifier = Column(String(50), nullable=False)
    species_id = Column(Integer, ForeignKey("pokemon_species.id"), nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    base_experience = Column(Integer, nullable=False)
    order = Column(Integer)
    is_default = Column(Boolean, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "identifier": self.identifier,
            "species_id": self.species_id,
            "height": self.height,
            "weight": self.weight,
            "base_experience": self.base_experience,
            "order": self.order,
            "is_default": self.is_default
        }


class PokemonStat(Base):
    __tablename__ = 'pokemon_stats'

    # pokemon_id,stat_id,base_stat,effort
    pokemon_id: Mapped[int] = mapped_column(Integer, ForeignKey('pokemon.id'), primary_key=True)
    stat_id: Mapped[int] = mapped_column(Integer, ForeignKey('stats.id'), primary_key=True)
    base_stat = Column(Integer, nullable=False)
    effort = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            "pokemon_id": self.pokemon_id,
            "stat_id": self.stat_id,
            "base_stat": self.base_stat,
            "effort": self.effort
        }


class PokemonType(Base):
    __tablename__ = 'pokemon_types'

    # pokemon_id,type_id,slot
    pokemon_id: Mapped[int] = mapped_column(Integer, ForeignKey('pokemon.id'), primary_key=True)
    type_id: Mapped[int] = mapped_column(Integer, ForeignKey('types.id'), primary_key=True)
    slot = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            "pokemon_id": self.pokemon_id,
            "type_id": self.type_id,
            "slot": self.slot
        }


class PokemonAbility(Base):
    __tablename__ = 'pokemon_abilities'

    # pokemon_id,ability_id,is_hidden,slot
    pokemon_id: Mapped[int] = mapped_column(Integer, ForeignKey('pokemon.id'), primary_key=True)
    ability_id: Mapped[int] = mapped_column(Integer, ForeignKey('abilities.id'), primary_key=True)
    is_hidden = Column(Boolean, nullable=False)
    slot = Column(Integer, nullable=False, primary_key=True)

    def to_dict(self):
        return {
            "pokemon_id": self.pokemon_id,
            "ability_id": self.ability_id,
            "is_hidden": self.is_hidden,
            "slot": self.slot
        }


class PokemonEggGroup(Base):
    __tablename__ = 'pokemon_egg_groups'

    # species_id,egg_group_id
    species_id: Mapped[int] = mapped_column(Integer, ForeignKey('pokemon_species.id'), primary_key=True)
    egg_group_id: Mapped[int] = mapped_column(Integer, ForeignKey('egg_groups.id'), primary_key=True)

    def to_dict(self):
        return {
            "species_id": self.species_id,
            "egg_group_id": self.egg_group_id
        }


class PokemonEvolution(Base):
    __tablename__ = 'pokemon_evolution'

    # id,evolved_species_id,evolution_trigger_id,trigger_item_id
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    evolved_species_id = Column(Integer, ForeignKey("pokemon_species.id"), nullable=False)
    evolution_trigger_id = Column(Integer, ForeignKey("evolution_triggers.id"), nullable=False)
    trigger_item_id = Column(Integer, ForeignKey("items.id"))

    # minimum_level,gender_id,location_id,held_item_id,time_of_day,known_move_id,known_move_type_id
    minimum_level = Column(Integer)
    gender_id = Column(Integer)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    held_item_id = Column(Integer, ForeignKey("items.id"), nullable=True)
    time_of_day = Column(String(10))
    known_move_id = Column(Integer, nullable=True)
    known_move_type_id = Column(Integer, nullable=True)

    # minimum_happiness,minimum_beauty,minimum_affection,relative_physical_stats,party_species_id,party_type_id,trade_species_id,needs_overworld_rain,turn_upside_down
    minimum_happiness = Column(Integer)
    minimum_beauty = Column(Integer)
    minimum_affection = Column(Integer)
    relative_physical_stats = Column(Integer)
    party_species_id = Column(Integer, ForeignKey("pokemon_species.id"), nullable=True)
    party_type_id = Column(Integer, ForeignKey("types.id"), nullable=True)
    trade_species_id = Column(Integer, ForeignKey("pokemon_species.id"), nullable=True)
    needs_overworld_rain = Column(Boolean)
    turn_upside_down = Column(Boolean)
