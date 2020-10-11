from django.shortcuts import render
from django.db.models import Sum
from basic_app.models import CurrentSeason, PastSeasons
from basic_app.api_functions import get_standings, week_scores, get_trophies, skittish, get_week, season_stats, league_graph_stats


def home(request):
    week = get_week()
    player = week_scores()
    score_dict = get_standings()
    t_and_l = get_trophies()
    trophies = t_and_l['trophies']
    dollars = t_and_l['dollars']
    skit = skittish()
    late_szn = CurrentSeason.stats.late_season()
    late_szn.reverse()

    return render(request, 'basic_app/home.html', {'week_scores': player,
                                                   'Scoreboard': score_dict,
                                                   'trophies': trophies,
                                                   'leaders': dollars,
                                                   'week': week,
                                                   'skittish': skit,
                                                   'late': late_szn
                                                   })


'''
- Week Scores: return list of [owner_name, [list of weekly scores for graphing]]
- Scoreboard: return list of [rank, team, W, L, PF, PA]
- Trophies: Dict of trophies with amount list as the value
'''


def season(request):
    stats = season_stats()
    return render(request, 'basic_app/season_stats.html', {'stats': stats})


def player_page(request, team_abbrev):
    base_team = CurrentSeason.objects.filter(year=2020)
    team = []
    weekly_place = []
    weeks = list(base_team.values_list('game_week', flat=True).distinct())

    for w in weeks:
        for idx, obj in enumerate(base_team.filter(game_week=w).order_by('-points_for')):
            if obj.team_abbrev == team_abbrev:
                team.append(obj.points_for)
                weekly_place.append((obj.points_for, idx+1))

    stats = league_graph_stats()
    hi, lo, avg = stats[0], stats[1], stats[2]
    return render(request, 'basic_app/player.html', {'team': team, "hi": hi, 'lo': lo, 'avg': avg, 'ranks':weekly_place})


def past(request):
    past_list = PastSeasons.objects.order_by('year').order_by('place').values()
    league_scores = PastSeasons.stats.league_points()
    for i in past_list:
        year = i['year']
        s_pt = league_scores[year]
        p_pt = i['points_for']
        dif = (p_pt - s_pt)/s_pt * 100
        pct_d = str(round(dif, 1)) + "%"
        i['pct_d'] = pct_d

        s_pt_ag = league_scores[year]
        p_pt_ag = i['points_against']
        dif_ag = (p_pt_ag - s_pt_ag)/s_pt_ag * 100
        pct_d_ag = str(round(dif_ag, 1)) + "%"
        i['pct_d_ag'] = pct_d_ag

    owners = PastSeasons.objects.distinct(
        'owner').values_list('owner', flat=True)
    totals = []
    # add current season wins and losses

    for player in owners:
        name = player
        current = CurrentSeason.objects.filter(
            year=2020, owner=player, game_week__lte=13)
        stats = PastSeasons.stats.player_stats(player)
        szn = list(current.aggregate(Sum('result')).values())[0]
        if type(szn) == int:
            cur_losses = current.count() - szn
            stats['wins'] += szn
            stats['losses'] += cur_losses
        pct = (stats['wins'] / (stats['wins'] + stats['losses'])) * 100
        pct = str(round(pct, 1)) + "%"
        stats['win_pct'] = pct
        stats['player'] = name

        scores = stats.pop('points_for_yr')
        avg = []
        for key in scores:
            dif = (scores[key] - league_scores[key]) / (league_scores[key])
            avg.append(dif)
        f_avg = sum(avg)/len(avg) * 100
        f_avg = str(round(f_avg, 2)) + "%"
        stats['pf_avg'] = f_avg

        scores_ag = stats.pop('points_ag_yr')
        avg_ag = []
        for key in scores_ag:
            dif = (scores_ag[key] - league_scores[key]) / (league_scores[key])
            avg_ag.append(dif)
        ag_avg = sum(avg_ag)/len(avg_ag) * 100
        ag_avg = str(round(ag_avg, 2)) + "%"
        stats['pa_avg'] = ag_avg
        stats['avg_place'] = round(stats['avg_place'], 2)
        totals.append(stats)
    return render(request, 'basic_app/past_seasons.html', {'past_szn': past_list, 'total': totals})
