from django.shortcuts import render
from django.db.models import Sum
from .models import CurrentSeason, PastSeasons, Player
from basic_app.espn_api import owners, scoreboard_dict, record, trophies, dollars, season_stats



# Create your views here.
def home(request):
    score_dict = scoreboard_dict(record)
    player = []
    for a in owners:
        scores = list(CurrentSeason.objects.filter(owner=a).order_by('game_week').values_list('poinst_for', flat=True))
        if len(scores)>0:
            player.append([a, scores])
    return render(request, 'basic_app/home.html', {'week_scores':player,
    'Scoreboard':score_dict, 'trophies':trophies, 'leaders':dollars})

def season(request):
    stats = season_stats()[0]
    return render(request, 'basic_app/season_stats.html', {'stats':stats})


def player_page(request, team_abbrev):
    team = CurrentSeason.objects.all().filter(team_abbrev=team_abbrev).values_list('poinst_for')
    for i in team:
        i = i[:-1]
    team = list(team)
    stats = season_stats()[1]
    hi, lo, avg = stats[0], stats[1], stats[2]
    return render(request, 'basic_app/player.html', {'team':team, "hi":hi, 'lo':lo, 'avg':avg})

def past(request):
    past_list = PastSeasons.objects.order_by('year')

    clist = list(PastSeasons.objects.values_list('owner', 'wins', 'losses'))
    totals = {}
    for c in clist:
        if c[0] in totals:
            totals[c[0]][0] += c[1]
            totals[c[0]][1] += c[2]
        else:
            totals[c[0]] = [c[1], c[2]]
    for key in totals.keys():
        szn = list(CurrentSeason.objects.filter(owner=key).aggregate(Sum('result')).values())[0]
        cur = totals[key]
        if type(szn) == int:
            cur[0] += szn
            cur[1] += (16 - szn)
        pct = "%.3f" % float(cur[0]/(cur[0] + cur[1]))
        totals[key].append(pct)

    return render(request, 'basic_app/past_seasons.html', {'past_szn': past_list, 'total':totals})
