from django.db import models


class Player(models.Model):
    player_name = models.CharField(max_length=100, unique=True, primary_key=True)

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


class CurrentSeason(models.Model):
    year = models.IntegerField()
    game_week = models.IntegerField()
    team_name = models.CharField(max_length=100, unique=False)
    team_abbrev = models.CharField(max_length=100, unique=False)
    poinst_for = models.FloatField()
    opponent = models.CharField(max_length=100, unique=False)
    points_against = models.FloatField()
    result = models.IntegerField(default=0)
    owner = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.game_week)


class Prize(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()

    def __str__(self):
        return models.name


class Skittish(models.Model):
    pass


# class Rankings(models.Model):
#     game_week = models.IntegerField()
#     team_name = models.CharField(max_length=100, unique=False)
#     team_abbrev = models.CharField(max_length=100, unique=False)
#     poinst_for = models.FloatField()
#     points_against = models.FloatField()
#     owner = models.ForeignKey(Player, on_delete=models.CASCADE)
#     place = models.IntegerField()
