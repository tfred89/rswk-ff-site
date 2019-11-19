from basic_app.models import Rankings, CurrentSeason, Player, Skittish
from basic_app.api_functions import get_week
from django.db.models import Min
from ff_espn_api import League



def weekly_db_update(league):
    week = league.nfl_week
    year = league.year
    comp = week - 1
    bs = league.box_scores(comp)
    for game in bs:
        home_score = game.home_score
        home_team = game.home_team

        away_score = game.away_score
        away_team = game.away_team
        diff = home_score - away_score
        if diff > 0:
            home_result = 1
            away_result = 0
        else:
            home_result = 0
            away_result = 1

        h_owner = Player.objects.get(player_id=home_team.team_id)
        a_owner = Player.objects.get(player_id=away_team.team_id)

        x, xx = CurrentSeason.objects.get_or_create(
            year=year,
            game_week=week,
            team_name=home_team.team_name,
            team_abbrev=home_team.team_abbrev,
            points_for=home_score,
            opponent=away_team.team_name,
            points_against=away_score,
            result=home_result,
            owner=h_owner)
        x.save()

        y, yy = CurrentSeason.objects.get_or_create(
            year=year,
            game_week=week,
            team_name=away_team.team_name,
            team_abbrev=away_team.team_abbrev,
            points_for=away_score,
            opponent=home_team.team_name,
            points_against=home_score,
            result=away_result,
            owner=a_owner)
        y.save()


def add_rankings(league):
    week = get_week() - 1
    year = league.year
    rankings = league.standings()
    rank_dict = dict(enumerate(rankings, start=1))
    for place, player in rank_dict.items():
        t_name = player.team_name
        t_abb = player.team_abbrev
        w = player.wins
        loss = player.losses
        owner = Player.objects.get(player_id=player.team_id)
        pf = round(player.points_for, 2)
        pa = round(player.points_against, 2)
        x, y = Rankings.objects.get_or_create(
            year=year,
            game_week=week,
            team_name=t_name,
            team_abbrev=t_abb,
            points_for=pf,
            points_against=pa,
            owner=owner,
            place=place,
            wins=w,
            losses=loss)
        x.save()


def update_skittish(week, year):
    players = Skittish.objects.filter(eliminated=False)
    p_ids = [p.player.player_id for p in players]
    week_scores = CurrentSeason.objects.filter(
        year=year, game_week=week, owner__player_id__in=p_ids)
    low_score = week_scores.aggregate(Min('points_for'))
    the_skitted = week_scores.get(points_for=low_score['points_for__min'])
    get_skit = Skittish.objects.get(player=the_skitted.owner)
    get_skit.eliminated=True
    get_skit.elim_score=low_score['points_for__min']
    get_skit.elim_week=week
    get_skit.save()


def weekly_update():
    year = 2019
    league_id = 1406490
    swid = '{CC3929FE-4B90-497B-87D7-6283A951436F}'
    espn_s2 = 'AECMpoZv%2FZF6G9Q1PEU9bnJD2Xf8FJwcFa8voarn81ZyGsMy8BzOpN8M6Wd9dLle3mHCQpW%2F0uQja23BYQagdA9H6tFSbtqGyyg%2BZs3m22Y%2FKNxo7os%2BBNSjX4bKa6UOSBlOph7KwtyMFBe654mVtR4inWzGYrTFVo2RIDk6ueNPFnz%2BDlKaxcQhRniwrEnXhprLfL78Gel1JetARL5lkiqGR2f%2BaPoxq%2Btfb8uj%2BzQAkMEkwJZaoWOUCPfxa7w%2FLa5GVnX5Ca%2F2ZqhFeysjWwOhYflDFnlItB1SKjpWPFtQ2w%3D%3D'
    league = League(league_id, year, espn_s2, swid)
    week = get_week() - 1
    weekly_db_update(league)
    add_rankings(league)
    update_skittish(week, 2019)
