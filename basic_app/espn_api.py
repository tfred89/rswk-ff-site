# import requests
# from espnff import League
# import pandas as pd
#
# from basic_app.models import CurrentSeason
#
# league_players = {
# 'STAN':'Ryan Stanley',
# 'TRLY':'Taylor Cannetti',
# 'TW':'Michael Welsh',
# 'JML':'Juan Lopez',
# 'FOX':'Ryan Fox',
# 'phil':'Trent Frederick',
# 'DICK':'Dickie Fischer',
# 'GODS':'Caleb Stiernagle',
# 'HATE':'Matthew Smith',
# "JJ's":'Justin Welsh',
# 'null':'Jeff Arn',
# 'TBUX':'Tyler Santiago',
# 'JERI':'Jeremi Mattern',
# 'DRAG':'Levi Laclair',
# 'EJF':'eduardo fischer'
# }
#
# owners = list(league_players.values())
#
# full = []
#
# endpoint = 'http://games.espn.com/ffl/api/v2/scoreboard'
#
# league_id = 1406490
# seasonId = 2018
# #league = League(league_id, seasonId)
#
# def gameweek(league): #finds currrent week
#         count = 1
#         current = False
#         while current == False and count < 17:
#              r = requests.get('http://games.espn.com/ffl/api/v2/scoreboard',
#                     params={'leagueId': league_id, 'seasonId': 2018, 'matchupPeriodId': count})
#              temp = r.json()
#              if temp['scoreboard']['matchups'][0]['winner'] == 'undecided':
#                      current = True
#                      break
#              else:
#                      count += 1
#         return count
#
# #gw = gameweek(league)
# gw = 17 #this is temporary, delete as needed
# def cur_db(gw):
#     frame = []
#     scores = {}
#     for week in range(1, gw):
#         r = requests.get('http://games.espn.com/ffl/api/v2/scoreboard',
#                         params={'leagueId': league_id, 'seasonId': 2018, 'matchupPeriodId': week})
#         scores[week] = r.json()
#
#     for key in scores:
#         temp = scores[key]['scoreboard']['matchups']
#         for match in temp:
#             if match['winner'] == "away":
#                 away = 1
#                 home = 0
#             else:
#                 away = 0
#                 home = 1
#             frame.append([key,
#                        match['teams'][0]['team']['teamAbbrev'],
#                        match['teams'][0]['team']['teamLocation'],
#                        match['teams'][0]['team']['teamNickname'],
#                        match['teams'][1]['team']['teamAbbrev'],
#                        match['teams'][0]['score'],
#                        match['teams'][1]['score'],
#                        home,
#                        match['teams'][1]['team']['teamAbbrev'],
#                        match['teams'][1]['team']['teamLocation'],
#                        match['teams'][1]['team']['teamNickname'],
#                        match['teams'][0]['team']['teamAbbrev'],
#                        match['teams'][1]['score'],
#                        match['teams'][0]['score'],
#                        away])
#
#     df = pd.DataFrame(frame, columns=['Week', 'HomeAbbrev', 'Home Location', 'Home Nickname', 'H Opponent', 'HomeScore', 'H Opponent Score',
#                                   'H Result','AwayAbbrev', 'Away Location', 'Away Nickname', 'A Opponent', 'AwayScore', 'A Opponent Score', 'A Result'])
#
#     df['Home Name'] = df['Home Location'] + df['Home Nickname']
#     df['Away Name'] = df['Away Location'] + df['Away Nickname']
#
#     df = (df[['Week', 'HomeAbbrev', 'Home Name', 'HomeScore', 'H Result', 'H Opponent', 'H Opponent Score']].rename(columns={'HomeAbbrev': 'Abbrev', 'HomeScore': 'Score', 'Home Name': 'Team Name', 'H Result':'Result', 'H Opponent':'Opponent', 'H Opponent Score':'Points against'}).append(df[['Week', 'AwayAbbrev', 'Away Name',
# 'AwayScore', 'A Result', 'A Opponent', 'A Opponent Score']].rename(columns={'AwayAbbrev': 'Abbrev', 'AwayScore': 'Score', 'Away Name':'Team Name', 'A Result':'Result', 'A Opponent':'Opponent', 'A Opponent Score':'Points against'})))
#
#     df['Owner'] = df['Abbrev'].map(league_players)
#
#     df_list = df.values.tolist()
#     return df
#
# def gw_db_update(gw):
#     frame = []
#     scores = {}
#     week = gw - 1
#     r = requests.get('http://games.espn.com/ffl/api/v2/scoreboard',
#                     params={'leagueId': league_id, 'seasonId': 2018, 'matchupPeriodId': week})
#     scores[week] = r.json()
#
#     for key in scores:
#         temp = scores[key]['scoreboard']['matchups']
#         for match in temp:
#             if match['winner'] == "away":
#                 away = 1
#                 home = 0
#             else:
#                 away = 0
#                 home = 1
#             frame.append([key,
#                        match['teams'][0]['team']['teamAbbrev'],
#                        match['teams'][0]['team']['teamLocation'],
#                        match['teams'][0]['team']['teamNickname'],
#                        match['teams'][1]['team']['teamAbbrev'],
#                        match['teams'][0]['score'],
#                        match['teams'][1]['score'],
#                        home,
#                        match['teams'][1]['team']['teamAbbrev'],
#                        match['teams'][1]['team']['teamLocation'],
#                        match['teams'][1]['team']['teamNickname'],
#                        match['teams'][0]['team']['teamAbbrev'],
#                        match['teams'][1]['score'],
#                        match['teams'][0]['score'],
#                        away])
#
#     df = pd.DataFrame(frame, columns=['Week', 'HomeAbbrev', 'Home Location', 'Home Nickname', 'H Opponent', 'HomeScore', 'H Opponent Score',
#                                   'H Result','AwayAbbrev', 'Away Location', 'Away Nickname', 'A Opponent', 'AwayScore', 'A Opponent Score', 'A Result'])
#
#     df['Home Name'] = df['Home Location'] + df['Home Nickname']
#     df['Away Name'] = df['Away Location'] + df['Away Nickname']
#
#     df = (df[['Week', 'HomeAbbrev', 'Home Name', 'HomeScore', 'H Result', 'H Opponent', 'H Opponent Score']].rename(columns={'HomeAbbrev': 'Abbrev', 'HomeScore': 'Score', 'Home Name': 'Team Name', 'H Result':'Result', 'H Opponent':'Opponent', 'H Opponent Score':'Points against'}).append(df[['Week', 'AwayAbbrev', 'Away Name',
# 'AwayScore', 'A Result', 'A Opponent', 'A Opponent Score']].rename(columns={'AwayAbbrev': 'Abbrev', 'AwayScore': 'Score', 'Away Name':'Team Name', 'A Result':'Result', 'A Opponent':'Opponent', 'A Opponent Score':'Points against'})))
#     df['Owner'] = df['Abbrev'].map(league_players)
#     df_list = df.values.tolist()
#     return df_list
#
#
# # db_load = cur_db(gw).values.tolist()
# # db_update = gw_db_update(gw)
# #
# clist = list(CurrentSeason.objects.values_list('game_week', 'team_name', 'team_abbrev', 'points_for', 'opponent', 'points_against', 'result', 'owner'))
# cols = ['Week', 'Team Name', 'Abbrev', 'Score', 'Opponent', 'Points against', 'Result', 'Owner']
# df = pd.DataFrame.from_records(clist, columns=cols)
#
# # df = cur_db(gw)
#
# df_list = df.values.tolist()
#
# df['Type'] = pd.Series(['Regular Season' if w<=13 else 'Playoff' for w in df['Week']])
# df['Margin'] = df['Score'] - df['Points against']
#
# dff = df[df['Week'] <= 13]
# df10 = df[df['Week'] >= 10]
# weeks10 = df10[df10['Score'] == df10['Score'].max()]['Abbrev'].values.tolist()
# wk1016 = weeks10[0]
#
#
#
#
# byAbbrev = df.groupby('Abbrev')
#
# byWeek = dff.groupby('Week')
#
# #To get total win loss table:
# tab = []
# teams = dff['Abbrev'].unique()
# for team in teams:
# 	wins = dff[dff['Abbrev'] == team]['Result'].sum()
# 	losses = (gw-1) - wins
# 	tab.append([team, wins, losses])
#
# #To get a win-loss data frame:
#
# record = [byAbbrev.sum()['Score'].sort_values(ascending = False), byAbbrev.sum()['Points against'].sort_values(ascending = False), byAbbrev.sum()['Result'].sort_values(ascending = False)]
# record = pd.DataFrame(record).transpose()
# record['Losses'] = (gw-1) - record['Result']
# record = record.sort_values(by="Result", ascending = False)
#
# def scoreboard_dict(record):
#     record = record.reset_index()
#     temp = record.values.tolist()
#     count = 1
#     for i in temp:
#         i[1] = "%.2f" % i[1]
#         i[2] = "%.2f" % i[2]
#         i[3] = int(i[3])
#         i[4] = int(i[4])
#         i.append(count)
#         count += 1
#     return temp
#
# #Trophies:
#
#
# first = record.index[0]
# high_points = record.sort_values(by='Score', ascending=False).index[0]
# second = record.index[1]
# third = record.index[2]
# best_miss = record.iloc[8:].sort_values(by='Score').index[-1]
# most_against = record.sort_values(by='Points against', ascending=False).index[0]
#
# hs = [0] #high score
# bl=[0] # highest scoring loss, but currently needs work
# margin=[0] # biggest margin of victory
# for index, row in dff.iterrows():
#     if row['Score'] > hs[0]:
#         hs = [row['Score'], row['Abbrev'], row['Week']]
#     if row['Result'] == 0:
#         if row['Score'] > bl[0]:
#             bl = [row['Score'], row['Abbrev'], row['Week']]
#     if row['Result'] == 1:
#         x = row['Score'] - row['Points against']
#         if x > margin[0]:
#             margin = [x, row['Abbrev'], row['Week']]
# margin[0] = "%.2f" % margin[0]
#
#
# trophies = {
# 'first':['$375', 'FoxBox'],
# 'second':['$100', 'phil'],
# 'third':['$50', 'DRAG'],
# 'season_winner':['$25', first],
# 'skittish':['$40', 'DRAG'],
# 'high_points':['$25', high_points],
# 'week10_16':['$20', 'DRAG'],
# 'highest_loss':['$10', bl[1], bl[0], bl[2]],
# 'high_score':['$10', hs[1], hs[0], hs[2]],
# 'margin':['$10', margin[1], margin[0], margin[2]],
# 'most_against':['$10', most_against],
# 'best_miss':['$25', best_miss]
# }
#
# leaders={}
# for key, values in trophies.items():
#     if values[1] in leaders:
#         leaders[values[1]]+=int(values[0][1:])
#     if values[1] not in leaders:
#         leaders[values[1]]=int(values[0][1:])
#
# dollars = []
# for key, value in leaders.items():
# 	temp = [key, value]
# 	dollars.append(temp)
#
#
# def skittish(league): # outputs dictionary with key=game week, value =[losing score, team name], along with a list of survivors
#     skitted = {}
#     out=[]
#     week = league.nfl_week
#     survivors = []
#     for w in range(1, week):
#         matchups = league.box_scores(w)
#         score = {}
#         for i in matchups:
#             if i.home_team.team_name not in skitted:
#                 score[i.home_team.team_name] = i.home_score
#             if i.away_team.team_name not in skitted:
#                 score[i.away_team.team_name] = i.away_score
#         if min(score, key=score.get) not in skitted:
#             skitted[min(score, key=score.get)] = [w, score[min(score, key=score.get)]]
#     for i in league.scoreboard(week=gameweek(league)+1):
#             if i.home_team.team_name not in skitted:
#                     survivors.append(i.home_team.team_name)
#             if i.away_team.team_name not in skitted:
#                     survivors.append(i.away_team.team_name)
#     for key, value in skitted.items():
#         temp = [key, value[0], value[1]]
#         out.append(temp)
#     return [out, survivors]
#
# #skit = skittish(league)
#
#
#
# def old_season_stats():
#     stats = []
#     h = []
#     l = []
#     a = []
#     for i in range(1, gw):
#         hi = df[df['Week']==i]['Score'].max()
#         h.append(hi)
#         lo = df[df['Week']==i]['Score'].min()
#         l.append(lo)
#         avg = df[df['Week']==i]['Score'].mean()
#         a.append(avg)
#         std = df[df['Week']==i]['Score'].std()
#         stats.append([i, hi, lo, avg, std])
#     graph_stats = [h,l,a]
#     for i in stats:
#         i[1] = "%.2f" % i[1]
#         i[2] = "%.2f" % i[2]
#         i[3] = "%.2f" % i[3]
#         i[4] = "%.2f" % i[4]
#     return [stats, graph_stats]
