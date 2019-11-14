# from .models import Player
#
# def add_variable_to_context(request):
#     player_list = Player.objects.all()
#     return {
#         'player_list': player_list
#     }
from .models import CurrentSeason

def add_variable_to_context(request):
    db = CurrentSeason.objects.all().filter(game_week=1, year=2019)
    player_list = [x.team_abbrev for x in db]
    return {
        'player_list': player_list
    }
