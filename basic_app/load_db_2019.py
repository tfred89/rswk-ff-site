# from .models import Rankings, CurrentSeason, Player, Skittish
# from .api_functions import league as espn_league
# from django.db.models import Min
# league_load = espn_league
# '''
# Update player model with player_id
# Update Current Season for 2019
# update rankings
# update skittish
# '''
#
#
# def add_player_ids(league):
#     teams = league.teams
#     count = 0
#     for i in teams:
#         id = i.team_id
#         name = i.owner
#         if name == 'Logan Ivy':
#             name = 'Justin Welsh'
#         p = Player.objects.get(player_name=name)
#         p.player_id and= id
#         p.save()
#         count += 1
#     print(f"{count} player ids added")
#
#
# # To update currentseason
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
#                 owner=h_owner,
#                 point_dif=diff)
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
#                 owner=a_owner,
#                 point_dif=diff)
#             count += 1
#             print(f'update success # {count}')
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
#         w = player.wins
#         l = player.losses
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
#             place=place,
#             wins=w,
#             losses=l)
#     print('rankings objects added')
#
#
# def load_skittish(league):
#     count=0
#     players = Player.objects.exclude(player_name='Jeff Arn')
#     for player in players:
#         Skittish.objects.create(
#                     player=player,
#                     eliminiated=False
#                     )
#         count += 1
#     print(f"{count} skittish objects created")
#
#
#
# # iterate through each week
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
#
#
# print('adding player Ids')
# add_player_ids(league_load)
# print('adding current season data')
# update_db_todate(league_load)
# print('adding rankings')
# add_rankings(league_load)
# print('creating skittish objects')
# load_skittish(league_load)
# print('updating skittish')
# for week in range(1,11):
#     update_skittish(week, 2019)
#     print(f"skittish week {week} updated")
