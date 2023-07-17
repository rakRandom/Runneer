"""Settings for the "runneer.py" file"""

# ====================== Importations =====================
try:
    import pygame

    from json import loads, dumps, load, dump
    from webbrowser import open as op
    from random import randint
    from sys import exit
except: raise ImportError

with open("data/config.json", "r") as configs:
    data = loads(configs.read())


# ======================= Constants =======================
GAME_NAME = data["GAME_NAME"]
GAME_ICON = data["GAME_ICON"]
ANIMATION_SPEED = data["ANIMATION_SPEED"]
BACKGROUND_SPEED = data["BACKGROUND_SPEED"]


# ======================== screen =========================
SCREEN_WIDTH = data["SCREEN_WIDTH"]
SCREEN_HEIGHT = data["SCREEN_HEIGHT"]


# ========================= clock =========================
FRAMES_PER_SECOND = data["FRAMES_PER_SECOND"]


# ========================= enemy =========================
SPAWN_RATE = data["SPAWN_RATE"]
EASY_SPEED = data["EASY_SPEED"]
MEDIUM_SPEED = data["MEDIUM_SPEED"]
HARD_SPEED = data["HARD_SPEED"]
FLY_RARITY = data["FLY_RARITY"]
SNAIL_ANIMATION_SPEED = data["SNAIL_ANIMATION_SPEED"]
FLY_ANIMATION_SPEED = data["FLY_ANIMATION_SPEED"]


# ========================= player ========================
JUMP_FORCE = data["JUMP_FORCE"] / (FRAMES_PER_SECOND ** 0.5)#-600 / (FRAMES_PER_SECOND) * ((FRAMES_PER_SECOND / 60) ** 0.5)
GRAVITY_ACCELERATION = data["GRAVITY_ACCELERATION"] / FRAMES_PER_SECOND






