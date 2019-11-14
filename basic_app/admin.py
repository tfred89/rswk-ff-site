from django.contrib import admin
from basic_app.models import PastSeasons, CurrentSeason, Player, Rankings, Skittish

# Register your models here.
admin.site.register(PastSeasons)
admin.site.register(CurrentSeason)
admin.site.register(Player)
admin.site.register(Rankings)
admin.site.register(Skittish)
