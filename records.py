import xlwt
from score import Score
from mods import mod_list_to_string
from main import get_user_best_scores


def scores_to_excel(score_list):
    title = ['成绩ID', '日期', '地图ID', '地图名', '难度名', 'Mods', 'PP', '准确率', 'Score', 'Rank', 'Combo', '300', '100',
             '50', 'Miss',
             '难度星级', 'Aim', 'Speed', 'Extreme', 'CS', 'AR', 'OD', 'HP']
    book = xlwt.Workbook()
    sheet = book.add_sheet('scores', cell_overwrite_ok=True)
    for i in range(len(title)):
        sheet.write(0, i, title[i])

    for j, score_info in enumerate(score_list):
        score = Score(score_info)
        content = []
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

        for i in range(len(content)):  # 循环写入
            sheet.write(j + 1, i, content[i])

    book.save('4A_59_record.xls')


all_scores = get_user_best_scores("4A_59")
scores_to_excel(all_scores)