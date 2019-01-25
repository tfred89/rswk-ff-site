from django.shortcuts import render
from django.db.models import Sum
from .models import CurrentSeason, PastSeasons
from basic_app.espn_api import scoreboard_dict, record, league, skit, trophies, dollars, season_stats



# Create your views here.
def home(request):
    score_dict = scoreboard_dict(record)
    skitted = skit[0]
    surv = skit[1]

    return render(request, 'basic_app/home1.html', {'Scoreboard':score_dict,
    'skit_in':skitted, 'survivor':surv, 'trophies':trophies, 'leaders':dollars})


def season(request):
    stats = season_stats()
    return render(request, 'basic_app/season_stats.html', {'stats':stats})

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
