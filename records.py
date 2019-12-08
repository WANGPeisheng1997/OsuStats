import xlwt
from score import Score
from mods import mod_list_to_string
import pickle
import time
from copy import deepcopy


def sort_score_list_by_property(score_list, property_name, reverse=False):
    return sorted(score_list, key=lambda score: float(score[property_name]), reverse=reverse)


def scores_to_excel(score_list, output_path):
    # preprocessing
    start_time = time.time()
    score_list_by_id = sort_score_list_by_property(score_list, "score_id")
    dynamic_ordered_score_list = []
    for score in score_list_by_id:
        replace = False
        for i in range(len(dynamic_ordered_score_list)):
            if score["beatmap_id"] == dynamic_ordered_score_list[i]["beatmap_id"]:
                dynamic_ordered_score_list[i] = score
                replace = True
                break
        if not replace:
            dynamic_ordered_score_list.append(score)
        dynamic_ordered_score_list = sort_score_list_by_property(dynamic_ordered_score_list, "pp", True)
        historical_bp = dynamic_ordered_score_list.index(score) + 1
        score["historical_bp"] = historical_bp

    for score in score_list_by_id:
        for i in range(len(dynamic_ordered_score_list)):
            if score["score_id"] == dynamic_ordered_score_list[i]["score_id"]:
                score["current_bp"] = i + 1
        if "current_bp" not in score:
            score["current_bp"] = ""

    score_list_by_pp = sort_score_list_by_property(score_list_by_id, "pp", True)
    end_time = time.time()
    print("Preprocessing time: %.2fs" % (end_time - start_time))

    # add title
    title = ['当前bp', '历史bp', '成绩ID', '日期', '地图ID', '地图名', '难度名', 'Mods', 'PP', '准确率', 'Score', 'Rank', 'Combo', '300', '100',
             '50', 'Miss',
             '难度星级', 'Aim', 'Speed', 'Extreme', 'CS', 'AR', 'OD', 'HP']
    width = [64, 64, 90, 140, 64, 280, 130, 64, 64, 64, 64, 45, 64, 45, 45, 45, 45, 64, 64, 64, 64, 45, 45, 45, 45]
    book = xlwt.Workbook()
    sheet = book.add_sheet('scores', cell_overwrite_ok=True)
    style = xlwt.XFStyle()
    al = xlwt.Alignment()
    al.horz = xlwt.Alignment.HORZ_CENTER
    al.vert = xlwt.Alignment.VERT_CENTER
    style.alignment = al
    style_float = deepcopy(style)
    style_float.num_format_str = "0.00"
    style_acc = deepcopy(style)
    style_acc.num_format_str = "0.00%"

    for i in range(len(title)):
        sheet.write(0, i, title[i], style)

    # add content
    start_time = time.time()
    for j, score_info in enumerate(score_list_by_pp):
        print("Fetching: %d/%d" % (j, len(score_list_by_pp)))
        # get full score & beatmap information
        score = Score(score_info)
        content = []
        content.append(score_info["current_bp"])
        content.append(score_info["historical_bp"])
        content.append(score.score_id)
        content.append(score.date)
        content.append(score.beatmap_id)
        content.append(score.beatmap.song_name)
        content.append(score.beatmap.difficulty_name)
        mod_names = mod_list_to_string(score.enabled_mods)
        if mod_names == "":
            mod_names = "None"
        content.append(mod_names)
        content.append(score.pp)
        content.append(score.acc)
        content.append(score.score)
        content.append(score.rank)
        content.append("%d/%d" % (score.maxcombo, score.beatmap.max_combo))
        content.append(score.count300)
        content.append(score.count100)
        content.append(score.count50)
        content.append(score.countmiss)
        content.append(score.beatmap.stars)
        content.append(score.beatmap.aim)
        content.append(score.beatmap.speed)
        content.append(abs(score.beatmap.aim - score.beatmap.speed) * 0.5)
        content.append(score.beatmap.cs)
        content.append(score.beatmap.ar)
        content.append(score.beatmap.od)
        content.append(score.beatmap.hp)

        for i in range(len(content)):
            if title[i] in ['PP', '难度星级', 'Aim', 'Speed', 'Extreme', 'CS', 'AR', 'OD', 'HP']:
                sheet.write(j + 1, i, content[i], style_float)
            elif title[i] in ['准确率']:
                sheet.write(j + 1, i, content[i], style_acc)
            else:
                sheet.write(j + 1, i, content[i], style)


    # set format
    for col, width_col in enumerate(width):
        sheet.col(col).width = int(256 * (width_col / 7))

    # save excel
    book.save(output_path)
    end_time = time.time()
    print("Fetching time: %.2fs" % (end_time - start_time))


if __name__ == "__main__":
    names = ["wenhuo", "4A_59", "wjy", "chakecai"]
    for name in names:
        file_name = "user_bp/" + name + ".dat"
        fr = open(file_name, "rb")
        best_scores = pickle.load(fr)
        fr.close()
        scores_to_excel(best_scores, "user_bp/" + name + ".xls")
