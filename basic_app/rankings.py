from basic_app.models import CurrentSeason, Rankings
import pandas as pd

# wip, add GW function and DB addition once list is created
def add_ranks():
    clist = list(CurrentSeason.objects.filter(year=2019).values_list('game_week',
                 'team_name', 'team_abbrev', 'poinst_for', 'opponent',
                 'points_against', 'result', 'owner'))
    cols = ['Week', 'Team Name', 'Abbrev', 'Score', 'Opponent', 'Points against', 'Result', 'Owner']
    df = pd.DataFrame.from_records(clist, columns=cols)
    byAbbrev = df.groupby('Abbrev')
    record = [byAbbrev.sum()['Score'].sort_values(ascending = False), byAbbrev.sum()['Points against'].sort_values(ascending = False), byAbbrev.sum()['Result'].sort_values(ascending = False)]
    record = pd.DataFrame(record).transpose()
    record['Losses'] = (gw-1) - record['Result']
    record = record.sort_values(by="Result", ascending = False)
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
