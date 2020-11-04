import datetime
from .models import CurrentSeason, Rankings, Skittish, Player


def get_week(sub=0):
    start = datetime.datetime(
        2020, 9, 14, 23, 0, 0, tzinfo=datetime.timezone.utc)  # league start date
    now = datetime.datetime.now(datetime.timezone.utc)
    week = (now-start).days//7 + 1
    week -= sub
    return week


def get_standings():
    gw = get_week()
    standings = Rankings.objects.filter(year=2020, game_week=gw)
    if standings.count() == 0:
        nw = gw - 1
        standings = Rankings.objects.filter(year=2020, game_week=nw)
    output = []
    for i in standings:
        x = [i.team_name, i.points_for, i.points_against,
             i.wins, i.losses, i.place]
        x[1] = "%.2f" % x[1]
        x[2] = "%.2f" % x[2]
        output.append(x)
    return output


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
