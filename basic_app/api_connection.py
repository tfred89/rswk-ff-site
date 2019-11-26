from ff_espn_api import League
#from basic_app.models import CurrentSeason, Player, PastSeasons
import pandas as pd
from datetime import date

year = 2019
league_id = 1406490
swid = '{CC3929FE-4B90-497B-87D7-6283A951436F}'
espn_s2 = 'AECMpoZv%2FZF6G9Q1PEU9bnJD2Xf8FJwcFa8voarn81ZyGsMy8BzOpN8M6Wd9dLle3mHCQpW%2F0uQja23BYQagdA9H6tFSbtqGyyg%2BZs3m22Y%2FKNxo7os%2BBNSjX4bKa6UOSBlOph7KwtyMFBe654mVtR4inWzGYrTFVo2RIDk6ueNPFnz%2BDlKaxcQhRniwrEnXhprLfL78Gel1JetARL5lkiqGR2f%2BaPoxq%2Btfb8uj%2BzQAkMEkwJZaoWOUCPfxa7w%2FLa5GVnX5Ca%2F2ZqhFeysjWwOhYflDFnlItB1SKjpWPFtQ2w%3D%3D'
league = League(league_id, year, espn_s2, swid)

# 2019 season load for week 4


def get_week(sub=0):
    start = date(2019, 9, 3) # league start date
    now = date.today()
    week = (now-start).days//7 + 1
    week -= sub
    return week


def box_scores(game_week):
    box_scores = league.box_scores(game_week)
    for g in box_scores:
        home_team = g.home_team
        away_team = g.away_team
        score = g.home_score - g.away_score
        if score > 0:
            home_win = 1
            away_win = 0
        else:
            home_win = 0
            away_win = 1

        home_update = CurrentSeason.objects.get_or_create(
            year=2019,
            game_week = game_week,
            team_name = home_team.team_name,
            team_abbrev = home_team.team_abbrev,
            points_for = g.home_score,
            opponent = away_team.team_name,
            points_against = g.away_score,
            result = home_win,
            owner = Player.objects.get(player_name=home_team.owner)
        )[0]
        home_update.save()

        away_update = CurrentSeason.objects.get_or_create(
            year=2019,
            game_week = game_week,
            team_name = away_team.team_name,
            team_abbrev = away_team.team_abbrev,
            points_for = g.away_score,
            opponent = home_team.team_name,
            points_against = g.home_score,
            result = away_win,
            owner = Player.objects.get(player_name=away_team.owner)
        )[0]
        away_update.save()


def player_obj(team):
    wins = team.wins
    losses = team.losses
    pf = team.points_for
    pa = team.points_against
    name = team.team_name
    out = {'w':wins, 'l':losses, 'pa':pa, 'pf':pf, 'name':name}
    return out
