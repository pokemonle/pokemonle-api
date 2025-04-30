from sqlalchemy import func
from sqlalchemy.orm import Session, aliased

from db.model import Pokemon, PokemonSpecies, Generation, \
    PokemonAbility, Ability, PokemonType, Type, PokemonEggGroup, EggGroup, PokemonStat, StatName, \
    PokemonEvolution, EvolutionTrigger, PokemonColor

ATTACK = 2
DEFENSE = 3
SPECIAL_ATTACK = 4
SPECIAL_DEFENSE = 5


def compare_pokemon(
        db: Session,
        found: PokemonSpecies, target: PokemonSpecies,
        lang: int
):
    options = {
        "db": db,
        "found": found,
        "target": target,
        "lang": lang
    }

    rate = distance(found.capture_rate, target.capture_rate, 0)

    result = {
        "answer": found.id == target.id,
        "type": _type(**options),
        "ability": ability(**options),
        "gen": generation(db, found, target),
        "color": color(db, found, target),
        "evo": evolution(**options),
        "stat": stat(**options),
        "breeding": {
            "egg_group": egg(**options),
            "capture_rate": {"key": rate["key"], "value": rate["value"]},
        }
        # **stat(**options),
    }

    return result


def color(
        db: Session,
        found: PokemonSpecies, target: PokemonSpecies,
):
    col = (
        db.query(PokemonColor).filter(PokemonColor.id == found.color_id).first()
    )

    if col:
        return {
            "key": col.identifier,
            "value": found.color_id == target.color_id,
            "id": found.color_id
        }

    return {}


def generation(
        db: Session,
        found: PokemonSpecies, target: PokemonSpecies,
) -> dict[str, bool]:
    gen = (
        db.query(Generation)
        .filter(Generation.id == found.generation_id)
        .first()
    )
    return {"identifier": gen.identifier, **distance(found.generation_id, target.generation_id, 1)} if gen else {}


def ability(
        db: Session,
        found: PokemonSpecies, target: PokemonSpecies,
        lang: int,
) -> list:
    tpa = aliased(PokemonAbility, name="tpa")
    found_abilities = (
        db.query(
            PokemonAbility.ability_id,
            db.query(tpa)
            .filter(tpa.pokemon_id == target.id)  # type: ignore
            .filter(tpa.ability_id == PokemonAbility.ability_id)
            .exists()
            .label("value"),
            Ability.identifier,
        )
        .join(Ability, PokemonAbility.ability_id == Ability.id)
        .filter(PokemonAbility.pokemon_id == found.id)
        # .distinct()
        .all()
    )

    return [{"key": name, "value": value, "id": ability_id} for ability_id, value, name in found_abilities]


def _type(
        db: Session,
        found: PokemonSpecies, target: PokemonSpecies,
        lang: int,
) -> list:
    tpt = aliased(PokemonType, name="tpt")
    found_types = (
        db.query(
            PokemonType.type_id,
            db.query(tpt)
            .filter(tpt.pokemon_id == target.id)  # type: ignore
            .filter(tpt.type_id == PokemonType.type_id)
            .exists()
            .label("value"),
            Type.identifier,
        )
        .join(Type, PokemonType.type_id == Type.id)
        .filter(PokemonType.pokemon_id == found.id)
        # .distinct()
        .all()
    )

    return [{"key": name, "value": value, "id": type_id} for type_id, value, name in found_types]


def egg(
        db: Session,
        found: PokemonSpecies, target: PokemonSpecies,
        lang: int,
) -> list:
    tpe = aliased(PokemonEggGroup, name="tpe")
    found_eggs = (
        db.query(
            PokemonEggGroup.egg_group_id,
            db.query(tpe)
            .filter(tpe.species_id == target.id)  # type: ignore
            .filter(tpe.egg_group_id == PokemonEggGroup.egg_group_id)
            .exists()
            .label("value"),
            EggGroup.identifier,
        )
        .join(EggGroup, PokemonEggGroup.egg_group_id == EggGroup.id)

        .filter(PokemonEggGroup.species_id == found.id)
        # .distinct()
        .all()
    )

    return [{"key": name, "value": value} for egg_group_id, value, name in found_eggs]


def evolution(
        db: Session,
        found: PokemonSpecies, target: PokemonSpecies,
        lang: int,
):
    tpe = aliased(PokemonEvolution, name="tpe")
    found_evo = (
        db.query(
            PokemonEvolution,
            db.query(tpe)
            .filter(tpe.evolved_species_id == target.id)  # type: ignore
            .filter(tpe.id == PokemonEvolution.id)
            .exists()
            .label("value"),
            EvolutionTrigger.identifier,
        )
        .join(EvolutionTrigger,
              PokemonEvolution.evolution_trigger_id == EvolutionTrigger.id)  # type: ignore
        # .filter(EvolutionTriggerProse.local_language_id == lang)
        .filter(PokemonEvolution.evolved_species_id == found.id)
        .first()
    )

    print(found_evo)

    return {"key": found_evo[2], "value": found_evo[1]} if found_evo else None


def stat(
        db: Session,
        found: PokemonSpecies, target: PokemonSpecies,
        lang: int,
) -> dict:
    f_stats = get_stats(db, found.id)
    t_stats = get_stats(db, target.id)

    f_total = sum([s["base_stat"] for s in f_stats])
    t_total = sum([s["base_stat"] for s in t_stats])

    return {
        "pow": {"key": found.id, **distance(f_total, t_total, 50)},
        "detail": [
            {
                **distance(stat["base_stat"], t_stats[i]["base_stat"], 10)
            }
            for i, stat in enumerate(f_stats)
        ]
    }


def get_stats(
        db: Session, pokemon_id: int
) -> list[dict]:
    stats = (
        db.query(PokemonStat)
        .filter(PokemonStat.pokemon_id == pokemon_id)
        .order_by(PokemonStat.stat_id)
        .all()
    )

    return [s.to_dict() for s in stats]


def get_stat_lang(db: Session, lang: int):
    data = db.query(StatName).filter(StatName.local_language_id == lang).all()

    # data list to dict stat_id -> name
    return {d.stat_id: d.name for d in data}


def distance(found: int, target: int, near: int | None) -> dict:
    if found == target:
        return {"key": found, "value": "equiv", "dis": "equiv"}
    else:
        return {
            "key": found,
            "value": "high" if found < target else "low",
            "dis": "far" if abs(found - target) > near else "near"
        }
