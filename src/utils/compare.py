from sqlalchemy import func
from sqlalchemy.orm import Session, aliased

from core.pokemon import PokemonDataStats
from db.model import Pokemon, PokemonSpecies, PokemonSpeciesName, PokemonColorName, PokemonHabitatName, GenerationName, \
    PokemonAbility, AbilityName, PokemonType, Type, TypeName, PokemonEggGroup, EggGroupProse, PokemonStat, StatName, \
    PokemonEvolution, EvolutionTriggerProse, PokemonColor

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
        "egg": egg(**options),
        "gen": generation(**options),
        "color": color(db, found, target),
        "capture_rate": {"key": rate["key"], "value": rate["value"]},
        "evo": evolution(**options),
        "stat": stat(**options),
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
        lang: int,
) -> dict[str, bool]:
    gen = (
        db.query(GenerationName)
        .filter(GenerationName.local_language_id == lang)
        .filter(GenerationName.generation_id == found.generation_id)
        .first()
    )
    return {"key": gen.name, **distance(found.generation_id, target.generation_id, 1)} if gen else {}


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
            AbilityName.name,
        )
        .join(AbilityName, PokemonAbility.ability_id == AbilityName.ability_id)
        .filter(AbilityName.local_language_id == lang)
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
            EggGroupProse.name,
        )
        .join(EggGroupProse, PokemonEggGroup.egg_group_id == EggGroupProse.egg_group_id)
        .filter(EggGroupProse.local_language_id == lang)
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
            EvolutionTriggerProse.name,
        )
        .join(EvolutionTriggerProse,
              PokemonEvolution.evolution_trigger_id == EvolutionTriggerProse.evolution_trigger_id)  # type: ignore
        .filter(EvolutionTriggerProse.local_language_id == lang)
        .filter(PokemonEvolution.evolved_species_id == found.id)
        .first()
    )

    return {"key": found_evo.name, "value": found_evo.value} if found_evo else None


def stat(
        db: Session,
        found: PokemonSpecies, target: PokemonSpecies,
        lang: int,
) -> dict:
    found_stats = get_stats(db, found.id)
    target_stats = get_stats(db, target.id)

    stat_lang = get_stat_lang(db, lang)

    return {
        "pow": {"key": found.id, **distance(found_stats.total(), target_stats.total(), 50)},
        "speed": {"key": found_stats.speed, **distance(found_stats.speed, target_stats.speed, 10)},
        "attack": {"key": stat_distance(found_stats.attack, found_stats.special_attack, stat_lang[ATTACK],
                                        stat_lang[SPECIAL_ATTACK]),
                   "value": (found_stats.attack > found_stats.special_attack) == (
                           found_stats.attack > target_stats.special_attack)},
        "defense": {"key": stat_distance(found_stats.defense, found_stats.special_defense, stat_lang[DEFENSE],
                                         stat_lang[SPECIAL_DEFENSE]),
                    "value": (found_stats.defense > found_stats.special_defense) == (
                            found_stats.defense > target_stats.special_defense)
                    },
    }


def get_stats(
        db: Session, pokemon_id: int
) -> PokemonDataStats | None:
    stats = (
        db.query(PokemonStat)
        .filter(PokemonStat.pokemon_id == pokemon_id)
        .order_by(PokemonStat.stat_id)
        .all()
    )

    if stats is None or len(stats) != 6:
        return None
    return PokemonDataStats(
        stats[0].base_stat,
        stats[1].base_stat,
        stats[2].base_stat,
        stats[3].base_stat,
        stats[4].base_stat,
        stats[5].base_stat,
    )


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


def stat_distance(l: int, r: int, l_str: int, r_str: int) -> str:
    if l == r:
        return f"{l_str}={r_str}"
    elif l > r:
        return f"{l_str}>{r_str}"
    else:
        return f"{l_str}<{r_str}"
