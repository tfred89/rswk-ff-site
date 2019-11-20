from django.contrib import admin
from basic_app.models import PastSeasons, CurrentSeason, Player, Rankings, Skittish


class RankingsA(admin.ModelAdmin):
    list_display = ['year', 'game_week', 'team_name', 'owner',
                    'place', 'wins', 'losses']
    search_fields = ['game_week',]
    list_filter = ('game_week', 'team_name', 'place',)


class PastSeasonsA(admin.ModelAdmin):
    list_display = ['year', 'place', 'team_name',
                    'owner', 'wins', 'losses', 'ties']
    search_fields = ['owner', 'year']
    list_filter = ('year', 'place', 'owner',)


class CSA(admin.ModelAdmin):
    list_display = ['year', 'game_week', 'team_name', 'points_for',
                    'points_against', 'owner', 'point_dif']
    search_fields = ['owner', 'team_name']


class SkittishA(admin.ModelAdmin):
    list_display = ['player', 'eliminated']
    search_fields = ['player',]



# Register your models here.
admin.site.register(PastSeasons, PastSeasonsA)
admin.site.register(CurrentSeason, CSA)
admin.site.register(Player)
admin.site.register(Rankings, RankingsA)
admin.site.register(Skittish, SkittishA)
