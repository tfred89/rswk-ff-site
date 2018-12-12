
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RSWKsite.settings")

import django
django.setup()


from basic_app.models import PastSeasons, CurrentSeason

from basic_app.espn_api import db_update



# def add_past(li):
#     stat = PastSeasons.objects.get_or_create(year=li[0], place=li[1],
#     team_name=li[2], owner=li[3], wins=li[5], losses=li[6], ties=li[7],
#     points_for=li[8], points_against=li[9])[0]
#
#     stat.save()
def add_cur(li):
    stat = CurrentSeason.objects.get_or_create(game_week=li[0], team_abbrev=li[1],
    team_name=li[2], poinst_for=li[3], opponent=li[5], result=li[4], points_against=li[6])[0]

    stat.save()



if __name__ == '__main__':
    print("populating script")
    # for li in past_seasons:
    #     add_past(li)
    for i in db_update:
        add_cur(i)

    print("populating complete")
