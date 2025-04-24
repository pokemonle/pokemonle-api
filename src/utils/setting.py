# -*-coding: utf-8 -*-
# @Time    : 2025/4/24 10:41
# @Author  : TyranitarX
from .redis import RedisClient


async def get_settings(redis: RedisClient, room):
    hardid = str(redis.hget(room, "hardid").decode('utf-8'))
    selectedGens = str(redis.hget(room, "selectedGens").decode('utf-8')).split(',')
    battleOpen = str(redis.hget(room, "battleOpen").decode('utf-8'))
    shapeOpen = str(redis.hget(room, "shapeOpen").decode('utf-8'))
    catchOpen = str(redis.hget(room, "catchOpen").decode('utf-8'))
    showGenArrow = str(redis.hget(room, "showGenArrow").decode('utf-8'))
    cheatOpen = str(redis.hget(room, "cheatOpen").decode('utf-8'))
    reverseDisplay = str(redis.hget(room, "reverseDisplay").decode('utf-8'))
    maxGuess = int(redis.hget(room, "maxGuess").decode('utf-8'))
    return {
        "hardid": hardid,
        "selectedGens": [is_true_str(item) for item in selectedGens],
        "battleOpen": battleOpen == "True",
        "shapeOpen": is_true_str(shapeOpen),
        "catchOpen": is_true_str(catchOpen),
        "showGenArrow": is_true_str(showGenArrow),
        "cheatOpen": is_true_str(cheatOpen),
        "reverseDisplay": is_true_str(reverseDisplay),
        "maxGuess": maxGuess,
    }


def is_true_str(s: str) -> bool:
    """
    Check if the string is 'True' or 'False'
    :param s: str
    :return: bool
    """
    return s == "True"
