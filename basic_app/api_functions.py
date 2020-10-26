import datetime
from .models import CurrentSeason, Rankings, Skittish, Player

#
# standings = league.standings()


def get_week(sub=0):
    start = datetime.datetime(
        2020, 9, 14, 23, 0, 0, tzinfo=datetime.timezone.utc)  # league start date
    now = datetime.datetime.now(datetime.timezone.utc)
    week = (now-start).days//7 + 1
    week -= sub
    return week


# def send_week(league):
#     return league.nfl_week


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


def get_standings():
    gw = get_week()
    standings = Rankings.objects.filter(year=2020, game_week=gw)
    output = []
    for i in standings:
        x = [i.team_name, i.points_for, i.points_against,
             i.wins, i.losses, i.place]
        x[1] = "%.2f" % x[1]
        x[2] = "%.2f" % x[2]
        output.append(x)
    return output


# def old_week_scores(league):
#     standings = league.standings()
#     show_weeks = league.nfl_week - 1
#     output = []
#     for i in standings:
#         adder = [i.team_name, i.scores[:show_weeks]]
#         output.append(adder)
#     return output


def week_scores():
    standings = CurrentSeason.objects.filter(year=2020)
    owners = Player.objects.exclude(player_id=15)
    output = []
    for player in owners:
        scores = standings.filter(owner=player)
        adder = [scores[0].team_name, list(
            scores.values_list('points_for', flat=True))]
        output.append(adder)
    average = ['Weekly Avg', CurrentSeason.stats.week_avg_list()]


    output.append(average)
    return output


def get_trophies():

    gw = get_week()
    # late_szn = CurrentSeason.stats.late_season()[-1]

    if gw < 14:
        scores = CurrentSeason.objects.filter(year=2020).order_by('-point_dif')
        gw = max(list(scores.values_list('game_week', flat=True).distinct()))
        margin = scores.first()
        margin_score = f'{round(margin.points_for - margin.points_against, 2)} pt win'
        standings = Rankings.objects.filter(game_week=gw)
        bl = scores.filter(result=0).order_by('-points_for')[0]
        most_points = standings.order_by('-points_for').first()
        most_against = standings.order_by('-points_against').first()
        big_week = scores.order_by('-points_for').first()
        big_miss = standings.filter(place__gte=9).order_by('-points_for').first()
    else:
        standings = Rankings.objects.filter(game_week=13)
        scores = CurrentSeason.objects.filter(
            year=2020, game_week__lte=13).order_by('-point_dif')
        margin = scores.first()
        bl = scores.filter(result=0).order_by('-points_for').first()
        most_points = standings.order_by('-points_for').first()
        most_against = standings.order_by('-points_against').first()
        big_week = scores.order_by('-points_for').first()
        big_miss = standings.filter(place__gte=9).order_by('-points_for')[0]
    skittish = Skittish.objects.filter(eliminated=False)
    if skittish.count() == 1:
        p = skittish.first()
        skit_team = p.player.rankings_set.last().team_name
    else:
        skit_team = 'TBD'

    trophies = {
        # after week 14 for places 1-3 based on most points for still in playoffs
        'first': ['$375', standings[0].team_name],
        'second': ['$100', standings[1].team_name],
        'third': ['$50', standings[2].team_name],
        'season_winner': ['$25', standings[0].team_name],
        'skittish': ['$40', 'TBD'],
        'high_points': ['$25', most_points.owner.currentseason_set.filter(year=2020).last().team_name],
        'best_miss': ['$25', big_miss.owner.currentseason_set.filter(year=2020).last().team_name],
        'week10_16': ['$20', 'TBD'],
        'highest_loss': ['$10', bl.owner.currentseason_set.filter(year=2020).last().team_name, bl.points_for, bl.game_week],
        'high_score': ['$10', big_week.owner.currentseason_set.filter(year=2020).last().team_name, big_week.points_for, big_week.game_week],
        'margin': ['$10', margin.owner.currentseason_set.filter(year=2020).last().team_name, margin_score, margin.game_week],
        'most_against': ['$10', most_against.owner.currentseason_set.filter(year=2020).last().team_name],

    }
    leaders = {}
    for key, values in trophies.items():
        if values[1] in leaders:
            leaders[values[1]] += int(values[0][1:])
        elif values[1] not in leaders:
            leaders[values[1]] = int(values[0][1:])

    dollars = []
    for key, value in leaders.items():
        temp = [key, value]
        dollars.append(temp)
    output = {'trophies': trophies, 'dollars': dollars}
    return output


# outputs dictionary with key=game week, value =[losing score, team name], along with a list of survivors
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


def skittish():
    all = Skittish.objects.filter()
    playing = all.filter(eliminated=False)
    losers = all.filter(eliminated=True).order_by('elim_week')
    skitted = []
    survivors = [p.player for p in playing]
    for p in losers:
        info = [p.elim_week, p.player, p.elim_score]
        skitted.append(info)
    return [skitted, survivors]


def season_stats():
    return CurrentSeason.stats.full_stats()


def league_graph_stats():
    s = CurrentSeason.stats.full_stats()
    h = []
    low = []
    a = []
    for week in s:
        h.append(week[1])
        low.append(week[2])
        a.append(week[3])
    return [h, low, a]
