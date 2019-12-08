import requests
import json
from enum import Enum
from score import Score
import pickle
import time
import os

key = "1a513545298a4bad0ef9e23b5df5950795ca7b42"


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


def save_user_info(user_name, user_info):
    user_info['timestamp'] = time.time()
    file_name = user_name + '_' + time.strftime("%Y%m%d_%H%M%S", time.localtime()) + '.dat'
    f = open('user_info/' + file_name, 'wb')
    pickle.dump(user_info, f)
    f.close()



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


def prn_obj(obj):
    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))

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


# display_user_info(user_info)
#
# user_info = get_user_info("chakecai")
# display_user_info(user_info)
#
# user_info = get_user_info("wjy")
# display_user_info(user_info)


# print_beatmap_common_mods_difficulty(1675834)


def get_user_best_scores(user_name, limit=100):
    url = "https://osu.ppy.sh/api/get_user_best"
    params_dict = {
        "k": key,
        "u": user_name,
        "limit": limit
    }
    response = requests.get(url, params=params_dict)
    all_score_info = json.loads(response.text)
    return all_score_info
    # count = 0
    # for score_info in all_score_info:
    #     count += 1
    #     score = Score(score_info)
    #     print("第%d位最好成绩:" % count)
    #     score.print_important_info()


def save_user_best_scores(user_name, all_score_info):
    file_name = "user_bp/" + user_name + ".dat"
    score_id_list = []
    best_scores = []
    if os.path.exists(file_name):
        fr = open(file_name, "rb")
        best_scores = pickle.load(fr)
        fr.close()
        for score_info in best_scores:
            score_id_list.append(int(score_info["score_id"]))
        score_id_list = set(score_id_list)

    for score_info in all_score_info:
        score_id = int(score_info["score_id"])
        if score_id not in score_id_list:
            best_scores.append(score_info)
            print("new high score!", score_info)

    print(len(best_scores))

    f = open(file_name, 'wb')
    pickle.dump(best_scores, f)
    f.close()

# fr = open('user_info/wenhuo_20191207_153751.dat', 'rb')
# data1 = pickle.load(fr)
# print(data1)

if __name__ == "__main__":
    names = ["wenhuo", "4A_59", "wjy", "chakecai"]
    for name in names:
        user_info = get_user_info(name)
        save_user_info(name, user_info)

        all_scores = get_user_best_scores(name)
        save_user_best_scores(name, all_scores)
