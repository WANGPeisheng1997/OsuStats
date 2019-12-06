import requests
import json
from enum import Enum

key = "1a513545298a4bad0ef9e23b5df5950795ca7b42"

class Mods(Enum):
    NoFail         = 1
    Easy           = 2
    TouchDevice    = 4
    Hidden         = 8
    HardRock       = 16
    SuddenDeath    = 32
    DoubleTime     = 64
    Relax          = 128
    HalfTime       = 256
    Nightcore      = 512 # Only set along with DoubleTime. i.e: NC only gives 576
    Flashlight     = 1024
    Autoplay       = 2048
    SpunOut        = 4096
    Relax2         = 8192 # Autopilot
    Perfect        = 16384 # Only set along with SuddenDeath. i.e: PF only gives 16416
    Key4           = 32768
    Key5           = 65536
    Key6           = 131072
    Key7           = 262144
    Key8           = 524288
    FadeIn         = 1048576
    Random         = 2097152
    Cinema         = 4194304
    Target         = 8388608
    Key9           = 16777216
    KeyCoop        = 33554432
    Key1           = 67108864
    Key3           = 134217728
    Key2           = 268435456
    ScoreV2        = 536870912
    LastMod        = 1073741824


def get_user_info(user_name, days_ago=None):
    url = "https://osu.ppy.sh/api/get_user"
    params_dict = {
        "k": key,
        "u": user_name,
        "event_days": days_ago
    }
    response = requests.get(url, params=params_dict)
    user_info = json.loads(response.text)[0]
    return user_info


def display_user_info(user_info):
    # print(user_info)
    items_to_display = {}
    items_to_display["用户名"] = user_info["username"]
    items_to_display["注册时间"] = user_info["join_date"]
    items_to_display["pp"] = user_info["pp_raw"]
    items_to_display["准确率"] = "%.2f%%" % float(user_info["accuracy"])
    items_to_display["世界排名"] = user_info["pp_rank"]
    items_to_display["国家排名"] = user_info["pp_country_rank"]
    items_to_display["总游戏次数"] = user_info["playcount"]
    hours = int(user_info["total_seconds_played"]) // 3600
    rest = int(user_info["total_seconds_played"]) % 3600
    items_to_display["总游戏时长"] = "%d小时%d分钟%d秒" % (hours, rest // 60, rest % 60)
    avg_time = int(user_info["total_seconds_played"]) / int(user_info["playcount"])
    items_to_display["平均游戏时长"] = "%d分钟%d秒" % (avg_time // 60, avg_time % 60)
    tth = int(user_info["count300"]) + int(user_info["count100"]) + int(user_info["count50"])
    items_to_display["总命中次数"] = tth
    avg_hit = tth / float(user_info["playcount"])
    items_to_display["平均命中次数"] = "%.2f" % avg_hit
    for k in items_to_display:
        print("%s: %s" % (k, items_to_display[k]))
    print()


def get_beatmap_info(map_id, mod_list):
    url = "https://osu.ppy.sh/api/get_beatmaps"
    mods = 0
    for mod in mod_list:
        mods += mod.value

    params_dict = {
        "k": key,
        "b": map_id,
        "mods": mods
    }
    response = requests.get(url, params=params_dict)
    beatmap_info = json.loads(response.text)[0]
    return beatmap_info


def print_beatmap_difficulty(beatmap_info):
    print("CS%.1f AR%.1f OD%.1f HP%.1f" % (float(beatmap_info["diff_size"]),
                                           float(beatmap_info["diff_approach"]),
                                           float(beatmap_info["diff_overall"]),
                                           float(beatmap_info["diff_drain"])))
    print("难度星级：%s" % beatmap_info["difficultyrating"])
    print("难度(aim)：%s" % beatmap_info["diff_aim"])
    print("难度(speed)：%s" % beatmap_info["diff_speed"])
    print()


def print_beatmap_common_mods_difficulty(map_id):
    mod_lists = [[], [Mods.HardRock], [Mods.Hidden], [Mods.HardRock, Mods.Hidden], [Mods.HalfTime], [Mods.DoubleTime]]
    for mod_list in mod_lists:
        beatmap_info = get_beatmap_info(map_id, mod_list)
        print("地图名：%s" % beatmap_info["title"])
        print("所选谱面：%s" % beatmap_info["version"])
        mod_name = [mod.name for mod in mod_list]
        if mod_name == []:
            mod_name = "None"
        else:
            mod_name = ','.join(name for name in mod_name)
        print("所选Mod：%s" % mod_name)
        print_beatmap_difficulty(beatmap_info)


user_info = get_user_info("wenhuo", "25")
display_user_info(user_info)

user_info = get_user_info("chakecai")
display_user_info(user_info)

user_info = get_user_info("wjy")
display_user_info(user_info)


# print_beatmap_common_mods_difficulty(1675834)
