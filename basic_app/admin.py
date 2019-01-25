from django.contrib import admin
from basic_app.models import PastSeasons, CurrentSeason, Player

# Register your models here.
admin.site.register(PastSeasons)
admin.site.register(CurrentSeason)
admin.site.register(Player)
