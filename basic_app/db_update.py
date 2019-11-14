# from .models import Rankings, CurrentSeason, Player, Skittish
# from .api_functions import league as espn_league
# from django.db.models import Min
#
#
# # TODO need a way to link player to model. Add tean_id?
# league_load = espn_league
#
#
# def update_db_todate(league):
#     week = league.nfl_week
#     year = league.year
#     count = 0
#     for i in range(1, week):
#         bs = league.box_scores(i)
#         for game in bs:
#             home_score = game.home_score
#             home_team = game.home_team
#
#             away_score = game.away_score
#             away_team = game.away_team
#             diff = home_score - away_score
#             if diff > 0:
#                 home_result = 1
#                 away_result = 0
#             else:
#                 home_result = 0
#                 away_result = 1
#             h_owner = Player.objects.get(player_id=home_team.team_id)
#             a_owner = Player.objects.get(player_id=away_team.team_id)
#
#             obj1, c1 = CurrentSeason.objects.get_or_create(
#                 year=year,
#                 game_week=i,
#                 team_name=home_team.team_name,
#                 team_abbrev=home_team.team_abbrev,
#                 points_for=home_score,
#                 opponent=away_team.team_name,
#                 points_against=away_score,
#                 result=home_result,
#                 owner=h_owner)
#             count += 1
#             print(f'update success # {count}')
#
#             obj2, c2 = CurrentSeason.objects.get_or_create(
#                 year=year,
#                 game_week=i,
#                 team_name=away_team.team_name,
#                 team_abbrev=away_team.team_abbrev,
#                 points_for=away_score,
#                 opponent=home_team.team_name,
#                 points_against=home_score,
#                 result=away_result,
#                 owner=a_owner)
#             count += 1
#             print(f'update success # {count}')
#
#
# def weekly_db_update(league):
#     week = league.nfl_week
#     year = league.year
#     comp = week - 1
#     bs = league.box_scores(comp)
#     for game in bs:
#         home_score = game.home_score
#         home_team = game.home_team
#
#         away_score = game.away_score
#         away_team = game.away_team
#         diff = home_score - away_score
#         if diff > 0:
#             home_result = 1
#             away_result = 0
#         else:
#             home_result = 0
#             away_result = 1
#
#         h_owner = Player.objects.get(player_id=home_team.team_id)
#         a_owner = Player.objects.get(player_id=away_team.team_id)
#
#         CurrentSeason.objects.create(
#             year=year,
#             game_week=week,
#             team_name=home_team.team_name,
#             team_abbrev=home_team.team_abbrev,
#             points_for=home_score,
#             opponent=away_team.team_name,
#             points_against=away_score,
#             result=home_result,
#             owner=h_owner)
#
#         CurrentSeason.objects.create(
#             year=year,
#             game_week=week,
#             team_name=away_team.team_name,
#             team_abbrev=away_team.team_abbrev,
#             points_for=away_score,
#             opponent=home_team.team_name,
#             points_against=home_score,
#             result=away_result,
#             owner=a_owner)
#
#
# def add_rankings(league):
#     week = league.nfl_week
#     year = league.year
#     rankings = league.standings()
#     rank_dict = dict(enumerate(rankings, start=1))
#     for place, player in rank_dict.items():
#         t_name = player.team_name
#         t_abb = player.team_abbrev
#         owner = Player.objects.get(player_id=player.team_id)
#         pf = round(player.points_for, 2)
#         pa = round(player.points_against, 2)
#         Rankings.objects.create(
#             year=year,
#             game_week=week,
#             team_name=t_name,
#             team_abbrev=t_abb,
#             points_for=pf,
#             points_against=pa,
#             owner=owner,
#             place=place)
#
#
# def update_skittish(week, year):
#     players = Skittish.objects.filter(eliminated=False)
#     p_ids = [p.player.player_id for p in players]
#     week_scores = CurrentSeason.objects.filter(
#         year=year, game_week=week, owner__player_id__in=p_ids)
#     low_score = week_scores.aggregate(Min('points_for'))
#     the_skitted = week_scores.get(points_for=low_score['points_for__min'])
#     get_skit = Skittish.objects.get(player=the_skitted.owner)
#     get_skit.eliminated=True
#     get_skit.elim_score=low_score['points_for__min']
#     get_skit.elim_week=week
#     get_skit.save()
