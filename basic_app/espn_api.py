import requests
from espnff import League
import pandas as pd
from .rswk_past import past_seasons

scores = {}
frame = []
full = []

endpoint = 'http://games.espn.com/ffl/api/v2/scoreboard'

league_id = 1406490
seasonId = 2018
league = League(league_id, seasonId)

def gameweek(league): #finds currrent week
        count = 1
        current = False
        while current == False:
             r = requests.get('http://games.espn.com/ffl/api/v2/scoreboard',
                    params={'leagueId': league_id, 'seasonId': 2018, 'matchupPeriodId': count})
             temp = r.json()
             if temp['scoreboard']['matchups'][0]['winner'] == 'undecided':
                     current = True
                     break
             else:
                     count += 1
        return count

gw = gameweek(league)

for week in range(1, gw):
    r = requests.get('http://games.espn.com/ffl/api/v2/scoreboard',
                    params={'leagueId': league_id, 'seasonId': 2018, 'matchupPeriodId': week})
    scores[week] = r.json()

for key in scores:
    temp = scores[key]['scoreboard']['matchups']
    for match in temp:
        if match['winner'] == "away":
            away = 1
            home = 0
        else:
            away = 0
            home = 1
        frame.append([key,
                   match['teams'][0]['team']['teamAbbrev'],
                   match['teams'][0]['team']['teamLocation'],
                   match['teams'][0]['team']['teamNickname'],
                   match['teams'][1]['team']['teamAbbrev'],
                   match['teams'][0]['score'],
                   match['teams'][1]['score'],
                   home,
                   match['teams'][1]['team']['teamAbbrev'],
                   match['teams'][1]['team']['teamLocation'],
                   match['teams'][1]['team']['teamNickname'],
                   match['teams'][0]['team']['teamAbbrev'],
                   match['teams'][1]['score'],
                   match['teams'][0]['score'],
                   away])

df = pd.DataFrame(frame, columns=['Week', 'HomeAbbrev', 'Home Location', 'Home Nickname', 'H Opponent', 'HomeScore', 'H Opponent Score',
                                  'H Result','AwayAbbrev', 'Away Location', 'Away Nickname', 'A Opponent', 'AwayScore', 'A Opponent Score', 'A Result'])

df['Home Name'] = df['Home Location'] + df['Home Nickname']
df['Away Name'] = df['Away Location'] + df['Away Nickname']

df = (df[['Week', 'HomeAbbrev', 'Home Name', 'HomeScore', 'H Result', 'H Opponent', 'H Opponent Score']].rename(columns={'HomeAbbrev': 'Abbrev', 'HomeScore': 'Score', 'Home Name': 'Team Name', 'H Result':'Result', 'H Opponent':'Opponent', 'H Opponent Score':'Points against'}).append(df[['Week', 'AwayAbbrev', 'Away Name',
'AwayScore', 'A Result', 'A Opponent', 'A Opponent Score']].rename(columns={'AwayAbbrev': 'Abbrev', 'AwayScore': 'Score', 'Away Name':'Team Name', 'A Result':'Result', 'A Opponent':'Opponent', 'A Opponent Score':'Points against'})))

df['Type'] = pd.Series(['Regular Season' if w<=13 else 'Playoff' for w in df['Week']])
df['Margin'] = df['Score'] - df['Points against']

dff = df[df['Week'] <= gw]
df10 = df[df['Week'] >= 10]
wk1016 = df10[df10['Score'] == df10['Score'].max()]['Abbrev'].values.tolist()[0]



byAbbrev = dff.groupby('Abbrev')
byWeek = dff.groupby('Week')
'''
#Possible dataframe manipulations to see various stats:
byAbbrev.mean()['Score'].sort_values(ascending = False)   # Sorts by highest average scores
byAbbrev.sum()['Score'].sort_values(ascending = False)  # Sorts by total points scored
byAbbrev.mean()['Points against'].sort_values(ascending = False)  # Sorts by highest average scores
byAbbrev.sum()['Points against'].sort_values(ascending = False)  # Sorts by total points scored
'''
#To get total win loss table:
tab = []
teams = dff['Abbrev'].unique()
for team in teams:
	wins = dff[dff['Abbrev'] == team]['Result'].sum()
	losses = (gw-1) - wins
	tab.append([team, wins, losses])

#To get a win-loss data frame:

record = [byAbbrev.sum()['Score'].sort_values(ascending = False), byAbbrev.sum()['Points against'].sort_values(ascending = False), byAbbrev.sum()['Result'].sort_values(ascending = False)]
record = pd.DataFrame(record).transpose()
record['Losses'] = (gw-1) - record['Result']
record = record.sort_values(by="Result", ascending = False)

def scoreboard_dict(record):
    record = record.reset_index()
    temp = record.values.tolist()
    count = 1
    for i in temp:
        i[1] = "%.2f" % i[1]
        i[2] = "%.2f" % i[2]
        i[3] = int(i[3])
        i[4] = int(i[4])
        i.append(count)
        count += 1
    temp
    return temp

#Trophies:


first = record.index[0]
high_points = record.sort_values(by='Score', ascending=False).index[0]
second = record.index[1]
third = record.index[2]
best_miss = record.iloc[8:].sort_values(by='Score').index[-1]
most_against = record.sort_values(by='Points against', ascending=False).index[0]

hs = [0] #high score
bl=[0] # highest scoring loss, but currently needs work
margin=[0] # biggest margin of victory
for index, row in dff.iterrows():
    if row['Score'] > hs[0]:
        hs = [row['Score'], row['Abbrev'], row['Week']]
    if row['Result'] == 0:
        if row['Score'] > bl[0]:
            bl = [row['Score'], row['Abbrev'], row['Week']]
    if row['Result'] == 1:
        x = row['Score'] - row['Points against']
        if x > margin[0]:
            margin = [x, row['Abbrev'], row['Week']]


trophies = {
'first':['$375', first],
'second':['$100', second],
'third':['$50', third],
'season_winner':['$25', first],
'skittish':['$40', 'TBD'],
'high_points':['$25', high_points],
'week10_16':['$20', wk1016],
'highest_loss':['$10', bl[1], bl[0], bl[2]],
'high_score':['$10', hs[1], hs[0], hs[2]],
'margin':['$10', margin[1], margin[0], margin[2]],
'most_against':['$10', most_against],
'best_miss':['$25', best_miss]
}

leaders={}
for key, values in trophies.items():
    if values[1] in leaders:
        leaders[values[1]]+=int(values[0][1:])
    if values[1] not in leaders:
        leaders[values[1]]=int(values[0][1:])

dollars = []
for key, value in leaders.items():
	temp = [key, value]
	dollars.append(temp)


def skittish(league): # outputs dictionary with key=game week, value =[losing score, team name], along with a list of survivors
    skitted = {}
    out=[]
    survivors = []
    for w in range(1, gameweek(league)):
        matchups = league.scoreboard(week=w)
        score = {}
        for i in matchups:
            if i.home_team.team_name not in skitted:
                score[i.home_team.team_name] = i.home_score
            if i.away_team.team_name not in skitted:
                score[i.away_team.team_name] = i.away_score
        if min(score, key=score.get) not in skitted:
            skitted[min(score, key=score.get)] = [w, score[min(score, key=score.get)]]
    for i in league.scoreboard(week=gameweek(league)+1):
            if i.home_team.team_name not in skitted:
                    survivors.append(i.home_team.team_name)
            if i.away_team.team_name not in skitted:
                    survivors.append(i.away_team.team_name)
    for key, value in skitted.items():
        temp = [key, value[0], value[1]]
        out.append(temp)
    return [out, survivors]

def season_stats():
    stats = []
    for i in range(1, gw):
        hi = dff[dff['Week']==i]['Score'].max()
        lo = dff[dff['Week']==i]['Score'].min()
        avg = dff[dff['Week']==i]['Score'].mean()
        std = dff[dff['Week']==i]['Score'].std()
        stats.append([i, hi, lo, avg, std])
    for i in stats:
        i[1] = "%.2f" % i[1]
        i[2] = "%.2f" % i[2]
        i[3] = "%.2f" % i[3]
        i[4] = "%.2f" % i[4]
    return stats
headers = ['Year', 'RANK', 'TEAM','OWNER(S)','REC','Wins','Losses','Ties','PF','PA','PF/G','PA/G']

past = pd.DataFrame(past_seasons, columns=headers)
szn2014 = past[past['Year'] == '2014'].values.tolist()
szn2015 = past[past['Year'] == '2015'].values.tolist()
szn2016 = past[past['Year'] == '2016'].values.tolist()
szn2017 = past[past['Year'] == '2017'].values.tolist()
past_szn = [szn2014, szn2015, szn2016, szn2017]
