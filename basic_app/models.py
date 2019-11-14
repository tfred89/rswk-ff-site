from django.db import models
from django.db.models import Avg, Max, Min, StdDev


class Player(models.Model):
    player_name = models.CharField(max_length=100, unique=True, primary_key=True)
    player_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.player_name


class PastSeasons(models.Model):
    year = models.IntegerField()
    place = models.IntegerField()
    team_name = models.CharField(max_length=100, unique=False)
    owner = models.ForeignKey(Player, on_delete=models.CASCADE)
    wins = models.IntegerField()
    losses = models.IntegerField()
    ties = models.IntegerField()
    points_for = models.FloatField()
    points_against = models.FloatField()


    def __str__(self):
        return str(self.year)


class CurrentSeasonCustom(models.QuerySet):

    def week_avg(self, gw):
        return self.filter(year=2019, game_week=gw).aggregate(Avg('points_for'))

    def week_avg_list(self):
        output = []
        weeks = self.filter(year=2019).values_list('game_week', flat=True).distinct()
        for w in weeks:
            num = self.week_avg(w)
            score = num.get('points_for__avg')
            output.append(score)
        return output

    def full_stats(self):
        weeks = list(self.filter(year=2019).values_list('game_week', flat=True).distinct())
        out = []
        for gw in weeks:
            qs = self.filter(year=2019, game_week=gw).aggregate(Max('points_for'), Min('points_for'), Avg('points_for'), StdDev('points_for'))
            adder = [round(i, 1) for i in qs.values()]
            adder = [gw] + adder
            out.append(adder)
        return out


class CurrentSeason(models.Model):
    year = models.IntegerField(blank=True, null=True)
    game_week = models.IntegerField()
    team_name = models.CharField(max_length=100, unique=False)
    team_abbrev = models.CharField(max_length=100, unique=False)
    points_for = models.FloatField() # changed from 'poinst', this may cause DB issues
    opponent = models.CharField(max_length=100, unique=False)
    points_against = models.FloatField()
    result = models.IntegerField(default=0)
    owner = models.ForeignKey(Player, on_delete=models.CASCADE)
    point_dif = models.FloatField(blank=True, null=True)

    objects = models.Manager()
    stats = CurrentSeasonCustom.as_manager()

    @property
    def margin(self):
        dif = self.points_for - self.points_against
        return dif

    def __str__(self):
        return 'GW ' + str(self.game_week)

    class Meta:
        ordering = ['-year', 'game_week']

# Needed models to eliminate constant espn API calls:
# Goes with function api_functions.get_standings


class Rankings(models.Model):
    year = models.IntegerField()
    game_week = models.IntegerField()
    team_name = models.CharField(max_length=100, unique=False)
    team_abbrev = models.CharField(max_length=100, unique=False)
    points_for = models.FloatField()
    points_against = models.FloatField()
    owner = models.ForeignKey(Player, on_delete=models.CASCADE)
    place = models.IntegerField()
    wins = models.IntegerField(blank=True, null=True)
    losses = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.place} place gw {self.game_week}"

    class Meta:
        ordering = ['game_week', 'place']


# For skittish, need to know all players, in/out, gameweek eliminated, score from GW eliminated
class Skittish(models.Model):
    player = models.ForeignKey(Player, models.CASCADE)
    eliminated = models.BooleanField(default=False)
    elim_score = models.FloatField(null=True, blank=True)
    elim_week = models.IntegerField(blank=True, null=True)
