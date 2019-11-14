# from datetime import date
# from .models import CurrentSeason, Rankings, Skittish, Player
# from ff_espn_api import League
#
# year = 2019
# league_id = 1406490
# swid = '{CC3929FE-4B90-497B-87D7-6283A951436F}'
# espn_s2 = 'AECMpoZv%2FZF6G9Q1PEU9bnJD2Xf8FJwcFa8voarn81ZyGsMy8BzOpN8M6Wd9dLle3mHCQpW%2F0uQja23BYQagdA9H6tFSbtqGyyg%2BZs3m22Y%2FKNxo7os%2BBNSjX4bKa6UOSBlOph7KwtyMFBe654mVtR4inWzGYrTFVo2RIDk6ueNPFnz%2BDlKaxcQhRniwrEnXhprLfL78Gel1JetARL5lkiqGR2f%2BaPoxq%2Btfb8uj%2BzQAkMEkwJZaoWOUCPfxa7w%2FLa5GVnX5Ca%2F2ZqhFeysjWwOhYflDFnlItB1SKjpWPFtQ2w%3D%3D'
# league = League(league_id, year, espn_s2, swid)
#
# standings = league.standings()
#
#
# def get_week():
#     start = date(2019, 9, 3) # league start date
#     now = date.today()
#     week = (now-start).days//7 + 1
#     return week
#
#
# # def send_week(league):
# #     return league.nfl_week
#
#
# def old_margin_and_loss(league):
#     week = league.nfl_week
#     obj = {'margin': [0, 0], 'big_loss': [0, 0]}
#     for i in range(1, week):
#         bs = league.box_scores(i)
#         for game in bs:
#             home_score = game.home_score
#             away_score = game.away_score
#             diff = home_score - away_score
#             if diff > obj['margin'][0]:
#                 obj['margin'] = [diff, game.home_score,
#                                  game.home_team.team_name, i]
#             elif diff < -obj['margin'][0]:
#                 obj['margin'] = [abs(diff), game.away_score,
#                                  game.away_team.team_name, i]
#             if diff > 0 and away_score > obj['big_loss'][0]:
#                 obj['big_loss'] = [away_score, game.away_team.team_name, i]
#             elif diff < 0 and home_score > obj['big_loss'][0]:
#                 obj['big_loss'] = [home_score, game.home_team.team_name, i]
#     return obj
#
#
# def old_get_standings(league):
#     standings = league.standings()
#     output = []
#     for i in standings:
#         x = [i.team_name, i.points_for, i.points_against,
#              i.wins, i.losses, i.standing]
#         x[1] = "%.2f" % x[1]
#         x[2] = "%.2f" % x[2]
#         output.append(x)
#     return output
#
#
# def get_standings():
#     gw = get_week() - 1
#     standings = Rankings.objects.filter(game_week=gw)
#     output = []
#     for i in standings:
#         x = [i.team_name, i.points_for, i.points_against,
#              i.wins, i.losses, i.place]
#         x[1] = "%.2f" % x[1]
#         x[2] = "%.2f" % x[2]
#         output.append(x)
#     return output
#
#
# def old_week_scores(league):
#     standings = league.standings()
#     show_weeks = league.nfl_week - 1
#     output = []
#     for i in standings:
#         adder = [i.team_name, i.scores[:show_weeks]]
#         output.append(adder)
#     return output
#
#
# def week_scores():
#     standings = CurrentSeason.objects.filter(year=2019)
#     owners = Player.objects.exclude(player_id=15)
#     output = []
#     for player in owners:
#         scores = standings.filter(owner=player)
#         adder = [scores[0].team_name, list(scores.values_list('points_for', flat=True))]
#         output.append(adder)
#     average = ['Weekly Avg', CurrentSeason.stats.week_avg_list()]
#     output.append(average)
#     return output
#
#
# def get_trophies():
#     gw = get_week() - 1
#     standings = Rankings.objects.filter(game_week=gw)
#     scores = CurrentSeason.objects.filter(year=2019).order_by('-point_dif')
#     margin = scores[0]
#     bl = scores.filter(result=0).order_by('-points_for')[0]
#     most_points = standings.order_by('-points_for')[0]
#     most_against = standings.order_by('-points_against')[0]
#     big_week = scores.order_by('-points_for')[0]
#
#     trophies = {
#         'first': ['$375', standings[0].team_name],
#         'second': ['$100', standings[1].team_name],
#         'third': ['$50', standings[2].team_name],
#         'season_winner': ['$25', standings[0].team_name],
#         'skittish': ['$40', 'TBD'],
#         'high_points': ['$25', most_points.team_name],
#         'week10_16': ['$20', 'TBD'],
#         'highest_loss': ['$10', bl.team_name, bl.points_for, bl.game_week],
#         'high_score': ['$10', big_week.team_name, big_week.points_for, big_week.game_week],
#         'margin': ['$10', margin.team_name, margin.points_for, margin.game_week],
#         'most_against': ['$10', most_against.team_name],
#         'best_miss': ['$25', 'TBD']
#     }
#     leaders = {}
#     for key, values in trophies.items():
#         if values[1] in leaders:
#             leaders[values[1]] += int(values[0][1:])
#         elif values[1] not in leaders:
#             leaders[values[1]] = int(values[0][1:])
#
#     dollars = []
#     for key, value in leaders.items():
#         temp = [key, value]
#         dollars.append(temp)
#     output = {'trophies': trophies, 'dollars': dollars}
#     return output
#
#
# # outputs dictionary with key=game week, value =[losing score, team name], along with a list of survivors
# def old_skittish(league):
#
#     week = league.nfl_week
#     skitted = []
#     weekly_dict = {}
#     losers = []
#
#     for w in range(1, week):
#         matchups = league.box_scores(w)
#         score = {}
#         for i in matchups:
#             ht = i.home_team.team_name
#             hs = i.home_score
#             if ht not in losers:
#                 score[ht] = hs
#             at = i.away_team.team_name
#             ascore = i.away_score
#             if at not in losers:
#                 score[at] = ascore
#         low_scorer = min(score.keys(), key=(lambda k: score[k]))
#         losers.append(low_scorer)
#         skit = [w, score.pop(low_scorer), low_scorer]
#         skitted.append(skit)
#         weekly_dict[w] = score
#     survivors = list(weekly_dict[week - 1].keys())
#
#     return [skitted, survivors]
#
#
# def skittish():
#     all = Skittish.objects.all()
#     playing = all.filter(eliminated=False)
#     losers = all.filter(eliminated=True)
#     skitted = []
#     survivors = [p.player for p in playing]
#     for p in losers:
#         info = [p.elim_week, p.player, p.elim_score]
#         skitted.append(info)
#     return [skitted, survivors]
