from beatmap import Beatmap
from mods import mod_list_to_val, val_to_mod_list, mod_list_to_string, Mods, AllMods
import math
import calculate_pp

class Score:
    def __init__(self, score_info):
        self.load_from_score_info(score_info)

    def load_from_score_info(self, score_info):
        self.beatmap_id = int(score_info["beatmap_id"])
        self.score_id = int(score_info["score_id"])
        self.score = int(score_info["score"])
        self.maxcombo = int(score_info["maxcombo"])
        self.count50 = int(score_info["count50"])
        self.count100 = int(score_info["count100"])
        self.count300 = int(score_info["count300"])
        self.countmiss = int(score_info["countmiss"])
        self.countkatu = int(score_info["countkatu"])
        self.countgeki = int(score_info["countgeki"])
        self.perfect = bool(int(score_info["perfect"]))
        self.enabled_mods = val_to_mod_list(int(score_info["enabled_mods"]))
        self.rank = score_info["rank"]
        self.user_id = int(score_info["user_id"])
        self.date = score_info["date"]
        self.rank = score_info["rank"]
        self.pp = float(score_info["pp"])
        self.replay_available = bool(int(score_info["replay_available"]))
        self.available_mods = []
        for mod in self.enabled_mods:
            if mod is not AllMods.Hidden:
                self.available_mods.append(mod)
        self.beatmap = Beatmap(map_id=self.beatmap_id, mod_list=self.available_mods)
        self.acc = calculate_pp.acc_calc(self.count300, self.count100, self.count50, self.countmiss)
        self.maxpp = calculate_pp.calculate_pp(beatmap=self.beatmap, c100=0, c50=0, misses=0,
                                               used_mods=Mods(mod_list_to_string(self.enabled_mods)),
                                               combo=None, score_version=1, c300=None).pp

    def print_important_info(self):
        print("日期：%s" % self.date)
        print("地图ID：%s" % self.beatmap_id)
        print("地图名：%s(%s)[+%s]" % (self.beatmap.song_name, self.beatmap.difficulty_name, mod_list_to_string(self.enabled_mods)))
        print("难度星级：%.2f (Aim:%.2f, Speed:%.2f, Extreme:%.2f)" % (self.beatmap.stars, self.beatmap.aim, self.beatmap.speed, abs(self.beatmap.aim-self.beatmap.speed) * 0.5))
        print("CS%.1f AR%.1f OD%.1f HP%.1f" % (float(self.beatmap.cs),
                                               float(self.beatmap.ar),
                                               float(self.beatmap.od),
                                               float(self.beatmap.hp)))
        print("==================================================")
        print("PP：%.2f (Max: %.2f)" % (self.pp, self.maxpp))
        print("准确率：%.2f%%" % (self.acc * 100))
        print("Rank：%s" % self.rank)
        print("Combo：%d/%d" % (self.maxcombo, self.beatmap.max_combo))
        print("300: %d, 100: %d, 50: %d" % (self.count300, self.count100, self.count50))
        print()