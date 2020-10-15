from basic_app.models import Player, CurrentSeason, PastSeasons, Rankings
from django.db.models import Avg, Max, Min, StdDev, Sum
from basic_app.api_functions import get_week

class PlayerInfo:

    def __init__(self, abbrev):
        self.player_abbrev = abbrev
        self.cs = CurrentSeason.objects.filter(year=2020, team_abbrev=abbrev)
        self.all_seasons = CurrentSeason.objects.filter(team_abbrev=abbrev)
        self.owner = self.cs.first().owner
        self.season_info = {}

    def avg_score(self):
        return self.cs.aggregate(Avg('points_for'))

    def avg_against(self):
        return self.cs.aggregate(Avg('points_against'))

    def weekly_results(self):
        weeks = get_week()
        self.weekly_points = []
        self.weekly_place = []
        self.top6 = 0
        self.bot6 = 0

        for i in range(1, weeks):
            for idx, obj in enumerate(CurrentSeason.objects.filter(year=2020, game_week=i).order_by('-points_for')):
                if obj.team_abbrev == self.player_abbrev:
                    self.weekly_points.append(obj.points_for)
                    place = idx + 1
                    self.weekly_place.append(place)
                    if place <= 6:
                        self.top6 += 1
                    else:
                        self.bot6 += 1

    def biggest_win(self):
        return self.cs.filter(result=1).aggregate(Max('point_dif'))

    def biggest_loss(self):
        return self.cs.filter(result=0).aggregate(Max('point_dif'))

    def close_win(self):
        return self.cs.filter(result=1).aggregate(Min('point_dif'))

    def close_loss(self):
        return self.cs.filter(result=0).aggregate(Min('point_dif'))

    def opponent_info(self, gw):
        pass
        
        
