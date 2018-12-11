from django.shortcuts import render
from .models import CurrentSeason, PastSeasons
from basic_app.espn_api import scoreboard_dict, record, league, skit, trophies, dollars, season_stats#, past_szn



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
    past_szn = {'past_szn': past_list}

    return render(request, 'basic_app/past_seasons.html', past_szn)
