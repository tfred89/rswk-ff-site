from .models import CurrentSeason


def add_variable_to_context(request):
    db = CurrentSeason.objects.all().filter(game_week=1, year=2020)
    player_set = set()
    for x in db:
        player_set.add(x.team_abbrev)
    player_list = list(player_set)
    return {
        'player_list': player_list
    }
