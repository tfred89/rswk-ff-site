from basic_app.models import Player, CurrentSeason, PastSeasons, Rankings
from django.db.models import Avg, Max, Min, StdDev, Sum
from basic_app.api_functions import get_week

'''
Example structure of 'PlayerInfo.info()'
{'avg_yearly_finish': 8.833333333333334,
  'current_place': 14,
  'wins': 0,
  'losses': 7,
  'avg_for': 92.1,
  'avg_against': 124.62,
  'biggest_win': None,
  'biggest_loss': -74.04,
  'closest_loss': 2.49,
  'closest_win': None,
  'avg_winning_score': None,
  'avg_losing_score': 92.1,
  'weekly_points': [100.03, 113.3, 74.32, 74.59, 85.92, 90.09, 106.46],
  'weekly_rank': [13, 9, 14, 13, 13, 10, 7],
  'avg_weekly_finish': 11.29,
  'top_7': 0,
  'bottom_7': 7,
  'player_id': 1,
  'player_abbrev': 'TBUX',
  'team_name': 'TBux DBest ',
  'hybrid_wins': 0,
  'hybrid_losses': 14}
'''


class PlayerInfo:

    def __init__(self, abbrev=None, id=None, year=2020):
        self.player_abbrev = abbrev
        self.year = year
        self.current_week = get_week()

        if id:
            self.id = id
            self.owner = Player.objects.get(player_id=id)
            self.cs = CurrentSeason.objects.filter(year=self.year, owner=self.owner)
            self.player_abbrev = self.cs.last().team_abbrev
            self.team_name = self.cs.last().team_name

        elif abbrev:
            self.owner = CurrentSeason.objects.filter(year=self.year, team_abbrev=abbrev).last().owner
            self.cs = CurrentSeason.objects.filter(year=self.year, owner=self.owner)
            self.team_name = self.cs.last().team_name
            self.id = self.owner.player_id

        self.all_seasons = CurrentSeason.objects.filter(owner=self.owner)
        self.season_info = {}


    def avg_score(self):
        avg_score = self.cs.aggregate(Avg('points_for'))
        score = avg_score.get('points_for__avg')
        self.season_info['avg_for'] = round(score, 2)
        return score

    def avg_against(self):
        avg_score =  self.cs.aggregate(Avg('points_against'))
        score = avg_score.get('points_against__avg')
        self.season_info['avg_against'] = round(score, 2)
        return score

    def biggest_win(self):
        win = list(self.cs.filter(result=1).values_list('point_dif', flat=True))
        win = [abs(i) for i in win]
        if len(win) > 0:
            score = round(max(win), 2)
        else:
            score = None
        self.season_info['biggest_win'] = score
        return score

    def biggest_loss(self):
        loss = list(self.cs.filter(result=0).values_list('point_dif', flat=True))
        loss = [abs(i) for i in loss]
        if len(loss) > 0:
            score = round(max(loss) * -1, 2)
        else:
            score = None
        self.season_info['biggest_loss'] = score
        return score

    def close_win(self):
        win = list(self.cs.filter(result=1).values_list('point_dif', flat=True))
        win = [abs(i) for i in win]
        if len(win) > 0:
            score = round(max(win), 2)
        else:
            score = None
        self.season_info['closest_win'] = score
        return score

    def close_loss(self):
        loss = list(self.cs.filter(result=0).values_list('point_dif', flat=True))
        loss = [abs(i) for i in loss]
        if len(loss) > 0:
            score = max(loss) * -1
            score = round(score, 2)
        else:
            score = None
        score = min(loss)
        self.season_info['closest_loss'] = score
        return score

    def win_avg_points(self):
        win = self.cs.filter(result=1).aggregate(Avg('points_for'))
        score = win.get('points_for__avg')
        if score:
            score = round(score, 2)
        self.season_info['avg_winning_score'] = score
        return score

    def loss_avg_points(self):
        loss = self.cs.filter(result=0).aggregate(Avg('points_for'))
        score = loss.get('points_for__avg')
        if score:
            score = round(score, 2)
        self.season_info['avg_losing_score'] = score
        return score

    def rank(self):
        rank = Rankings.objects.filter(owner=self.owner, year=self.year).last()
        avg_season_finish = PastSeasons.objects.filter(owner=self.owner).aggregate(Avg('place'))
        avg_place = avg_season_finish.get('place__avg')
        self.season_info['avg_yearly_finish'] = round(avg_place, 1)
        self.season_info['current_place'] = rank.place
        self.season_info['wins'] = rank.wins
        self.season_info['losses'] = rank.losses
        self.season_info['points_for'] = rank.points_for
        self.season_info['points_against'] = rank.points_against
        return rank

    def weekly_results(self):
        weeks = self.current_week if self.current_week < 17 else 16
        self.weekly_points = []
        self.weekly_place = []
        combined = []
        self.top7 = 0
        self.bot7 = 0

        base_cs = CurrentSeason.objects.filter(year=2020)

        for i in range(1, weeks+1):
            for idx, obj in enumerate(base_cs.filter(game_week=i).order_by('-points_for')):
                if obj.owner == self.owner:
                    self.weekly_points.append(obj.points_for)
                    place = idx + 1
                    self.weekly_place.append(place)
                    info = (i, obj.points_for, place)
                    combined.append(info)
                    if place <= 7:
                        self.top7 += 1
                    else:
                        self.bot7 += 1

        self.season_info['weekly_points'] = self.weekly_points
        self.season_info['weekly_rank'] = self.weekly_place
        self.season_info['avg_weekly_finish'] = round(sum(self.weekly_place)/len(self.weekly_place), 2)
        self.season_info['top_7'] = self.top7
        self.season_info['bottom_7'] = self.bot7
        self.season_info['combined_score_rank'] = combined


    def info(self):
        self.rank()
        self.avg_score()
        self.avg_against()
        self.biggest_win()
        self.biggest_loss()
        self.close_loss()
        self.close_win()
        self.win_avg_points()
        self.loss_avg_points()
        self.weekly_results()

        self.season_info['player_id'] = self.id
        self.season_info['player_abbrev'] = self.player_abbrev
        self.season_info['team_name'] = self.team_name
        
        hybrid_wins = self.season_info['wins'] + self.top7
        hybrid_losses = self.season_info['losses'] + self.bot7
        self.season_info['hybrid_wins'] = hybrid_wins
        self.season_info['hybrid_losses'] = hybrid_losses

        return self.season_info




        
        
