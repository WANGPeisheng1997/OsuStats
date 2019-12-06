import requests
import json
from enum import Enum
from mods import mod_list_to_val, mod_list_to_string, Mods, AllMods
import math

key = "1a513545298a4bad0ef9e23b5df5950795ca7b42"

class Approved_state(Enum):
    loved = 4
    qualified = 3
    approved = 2
    ranked = 1
    pending = 0
    WIP = -1
    graveyard = -2


class Genre(Enum):
    any = 0
    unspecified = 1
    videogame = 2
    anime = 3
    rock = 4
    pop = 5
    other = 6
    novelty = 7
    hiphop = 9
    electronic = 10


class Language(Enum):
    any = 0
    other = 1
    english = 2
    japanese = 3
    chinese = 4
    instrumental = 5
    korean = 6
    french = 7
    german = 8
    swedish = 9
    spanish = 10
    italian = 11


class Mode(Enum):
    standard = 0
    taiko = 1
    ctb = 2
    mania = 3


class Beatmap:
    def __init__(self, map_id, mod_list):
        self.load_from_beatmap_id(map_id, mod_list)

    def load_from_beatmap_id(self, map_id, mod_list):
        url = "https://osu.ppy.sh/api/get_beatmaps"
        mod_value = mod_list_to_val(mod_list)
        params_dict = {
            "k": key,
            "b": map_id,
            "mods": mod_value
        }
        response = requests.get(url, params=params_dict)
        beatmap_info = json.loads(response.text)[0]
        self.load_from_beatmap_info(beatmap_info)
        self.apply_mods(mod_list)


    def load_from_beatmap_info(self, beatmap_info):
        self.approved_state = Approved_state(int(beatmap_info["approved"]))
        self.submit_date = beatmap_info["submit_date"]
        self.approved_date = beatmap_info["approved_date"]
        self.last_update = beatmap_info["last_update"]
        self.artist = beatmap_info["artist"]
        self.beatmap_id = int(beatmap_info["beatmap_id"])
        self.beatmapset_id = int(beatmap_info["beatmapset_id"])
        self.bpm = float(beatmap_info["bpm"])
        self.creator = beatmap_info["creator"]
        self.creator_id = int(beatmap_info["creator_id"])
        self.stars = float(beatmap_info["difficultyrating"])
        self.aim = float(beatmap_info["diff_aim"])
        self.speed = float(beatmap_info["diff_speed"])
        self.cs = float(beatmap_info["diff_size"])
        self.od = float(beatmap_info["diff_overall"])
        self.ar = float(beatmap_info["diff_approach"])
        self.hp = float(beatmap_info["diff_drain"])
        self.hit_length = int(beatmap_info["hit_length"]) # not including breaks
        self.total_length = int(beatmap_info["total_length"]) # including breaks
        self.source = beatmap_info["source"]
        self.genre = Genre(int(beatmap_info["genre_id"]))
        self.language = Language(int(beatmap_info["language_id"]))
        self.song_name = beatmap_info["title"]
        self.difficulty_name = beatmap_info["version"]
        self.file_md5 = beatmap_info["file_md5"]
        self.playcount = int(beatmap_info["playcount"])
        self.passcount = int(beatmap_info["passcount"])
        self.count_normal = int(beatmap_info["count_normal"])
        self.count_slider = int(beatmap_info["count_slider"])
        self.count_spinner = int(beatmap_info["count_spinner"])
        self.num_objects = self.count_normal + self.count_slider + self.count_spinner
        self.max_combo = int(beatmap_info["max_combo"])
        self.mode = Mode(int(beatmap_info["mode"]))
        self.tags = beatmap_info["tags"].split(" ")
        self.favourite_count = int(beatmap_info["favourite_count"])
        self.rating = float(beatmap_info["rating"])
        self.download_unavailable = bool(int(beatmap_info["download_unavailable"]))
        self.audio_unavailable = bool(int(beatmap_info["audio_unavailable"]))

    def print_all_info(self):
       print('\n'.join(['%s: %s' % item for item in self.__dict__.items()]))

    def apply_mods(self, mod_list):
        mods = Mods(mod_list_to_string(mod_list))

        # Ugly shouldput somewhere else
        od0_ms = 79.5
        od10_ms = 19.5
        ar0_ms = 1800
        ar5_ms = 1200
        ar10_ms = 450

        od_ms_step = 6.0
        ar_ms_step1 = 120.0
        ar_ms_step2 = 150.0

        # If no mods affecting beatmap values are used
        # FL, SO, NF
        if not mods.map_changing:
           return

        speed = 1

        if mods.dt or mods.nc:
           speed *= 1.5

        if mods.ht:
           speed *= 0.75

        od_multiplier = 1
        if mods.hr:
           od_multiplier *= 1.4
        if mods.ez:
           od_multiplier *= 0.5

        self.od *= od_multiplier
        odms = od0_ms - math.ceil(od_ms_step * self.od)

        ar_multiplier = 1

        if mods.hr:
           ar_multiplier = 1.4

        if mods.ez:
           ar_multiplier = 0.5

        self.ar *= ar_multiplier

        arms = (ar0_ms - ar_ms_step1 * self.ar) if self.ar <= 5 else (ar5_ms - ar_ms_step2 * (self.ar - 5))

        cs_multipier = 1

        if mods.hr:
           cs_multipier = 1.3

        if mods.ez:
           cs_multipier = 0.5

        odms = min(od0_ms, max(od10_ms, odms))
        arms = min(ar0_ms, max(ar10_ms, arms))

        odms /= speed
        arms /= speed

        self.od = (od0_ms - odms) / od_ms_step
        self.ar = ((ar0_ms - arms) / ar_ms_step1) if self.ar <= 5.0 else (5.0 + (ar5_ms - arms) / ar_ms_step2)
        self.cs *= cs_multipier
        self.cs = max(0.0, min(10.0, self.cs))


# bp = Beatmap(1674283, [])
# bp.print_all_info()