from django.shortcuts import render
from basic_app.espn_api import scoreboard_dict, record, league, skittish, trophies, dollars, season_stats, past_szn

# Create your views here.
def home(request):
    score_dict = scoreboard_dict(record)
    skit = skittish(league)[0]
    surv = skittish(league)[1]

    return render(request, 'basic_app/home1.html', {'Scoreboard':score_dict,
    'skit_in':skit, 'survivor':surv, 'trophies':trophies, 'leaders':dollars})


def season(request):
    stats = season_stats()
    return render(request, 'basic_app/season_stats.html', {'stats':stats})

def past(request):
    return render(request, 'basic_app/past_seasons.html', {'past_szn': past_szn})
