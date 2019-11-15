from django.shortcuts import render
from django.db.models import Sum
from .models import CurrentSeason, PastSeasons
from basic_app.api_functions import get_standings, week_scores, get_trophies, skittish, get_week, season_stats, league_graph_stats


def home(request):
    player = week_scores()
    score_dict = get_standings()
    t_and_l = get_trophies()
    trophies = t_and_l['trophies']
    dollars = t_and_l['dollars']
    skit = skittish()
    week = get_week()
    return render(request, 'basic_app/home.html', {'week_scores': player,
                                                   'Scoreboard': score_dict,
                                                   'trophies': trophies,
                                                   'leaders': dollars,
                                                   'week': week,
                                                   'skittish': skit}
                                                   )


'''
- Week Scores: return list of [owner_name, [list of weekly scores for graphing]]
- Scoreboard: return list of [rank, team, W, L, PF, PA]
- Trophies: Dict of trophies with amount list as the value
'''


def season(request):
    stats = season_stats()
    return render(request, 'basic_app/season_stats.html', {'stats': stats})


def player_page(request, team_abbrev):
    team = list(CurrentSeason.objects.all().filter(year=2019, team_abbrev=team_abbrev).order_by(
        'game_week').values_list('points_for', flat=True))
    stats = league_graph_stats()
    hi, lo, avg = stats[0], stats[1], stats[2]
    return render(request, 'basic_app/player.html', {'team': team, "hi": hi, 'lo': lo, 'avg': avg})


def past(request):
    past_list = PastSeasons.objects.order_by('year').order_by('place')

    clist = list(PastSeasons.objects.values_list('owner', 'wins', 'losses'))
    totals = {}
    # add items to dict
    for c in clist:
        if c[0] in totals:
            totals[c[0]][0] += c[1]
            totals[c[0]][1] += c[2]
        else:
            totals[c[0]] = [c[1], c[2]]
    # add current season wins and losses
    for key in totals.keys():
        current = CurrentSeason.objects.filter(year=2019, owner=key)
        cur = totals[key]
        szn = list(current.aggregate(Sum('result')).values())[0]
        if type(szn) == int:
            cur_losses = szn - len(current)
            cur[0] += szn
            cur[1] += cur_losses
        pct = (cur[0] / (cur[0] + cur[1])) * 100
        pct = str(round(pct, 1)) + "%"
        totals[key].append(pct)
    sorted_totals = [[k, v] for k, v in totals.items()]
    st = []
    for i in sorted_totals:
        x = [i[0]] + i[1]
        st.append(x)
    st.sort(key=lambda x: x[3], reverse=True)
    return render(request, 'basic_app/past_seasons.html', {'past_szn': past_list, 'total': st})
