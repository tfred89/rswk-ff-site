
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RSWKsite.settings")

import django
django.setup()

from ff_espn_api import League
from basic_app.models import PastSeasons, CurrentSeason, Player



def add_past():
    year = 2019
    league_id = 1406490
    swid = '{CC3929FE-4B90-497B-87D7-6283A951436F}'
    espn_s2 = 'AECMpoZv%2FZF6G9Q1PEU9bnJD2Xf8FJwcFa8voarn81ZyGsMy8BzOpN8M6Wd9dLle3mHCQpW%2F0uQja23BYQagdA9H6tFSbtqGyyg%2BZs3m22Y%2FKNxo7os%2BBNSjX4bKa6UOSBlOph7KwtyMFBe654mVtR4inWzGYrTFVo2RIDk6ueNPFnz%2BDlKaxcQhRniwrEnXhprLfL78Gel1JetARL5lkiqGR2f%2BaPoxq%2Btfb8uj%2BzQAkMEkwJZaoWOUCPfxa7w%2FLa5GVnX5Ca%2F2ZqhFeysjWwOhYflDFnlItB1SKjpWPFtQ2w%3D%3D'
    league = League(league_id, year, espn_s2, swid)
    for owner in league.standings():
        if owner.owner == 'Logan Ivy':
            own = Player.objects.get(player_name='Justin Welsh')
        else:
            own = Player.objects.get(player_name=owner.owner)
        stat = PastSeasons.objects.get_or_create(
            year=2019, 
            place=owner.final_standing, 
            team_name=owner.team_name, 
            owner=own, 
            wins=owner.wins, 
            losses=owner.losses, 
            points_for=owner.points_for,
            ties=0, 
            points_against=owner.points_against)[0]
        stat.save()
        print(f'{owner.owner} added to database')




if __name__ == '__main__':
    print("populating script")
    add_past()
    print("populating complete")
