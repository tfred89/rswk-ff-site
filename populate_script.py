
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RSWKsite.settings")

import django
django.setup()


from basic_app.models import PastSeasons, CurrentSeason, Player
from basic_app.rswk_past import past_seasons
from basic_app.espn_api import db_update, db_load, owners

def add_player(li):
    stat = Player.objects.get_or_create(player_name=li)[0]
    stat.save()

def add_past(li):

    stat = PastSeasons.objects.get_or_create(year=int(li[0]), place=int(li[1]), team_name=li[2], owner=Player(pk=li[3]), wins=int(li[5]), losses=int(li[6]), ties=int(li[7]), points_for=float(li[8]), points_against=float(li[9]))[0]
    stat.save()

def add_cur(li):
    stat = CurrentSeason.objects.get_or_create(game_week=li[0], team_abbrev=li[1], team_name=li[2], poinst_for=li[3], opponent=li[5], result=li[4], points_against=li[6], owner=Player(pk=li[7]))[0]

    stat.save()



if __name__ == '__main__':
    print("populating script")
    p_count = 0
    s_count = 0
    for p in owners:
        add_player(p)
        p_count += 1
    print("%s records added to Players" % p_count)
    for li in past_seasons:
        add_past(li)
        s_count += 1
        print("past season added year: %s player: %s" %(li[0], li[3]))
    print("%s records added to Past Seasons" % s_count)
    for i in db_load:
        add_cur(i)


    print("populating complete")
