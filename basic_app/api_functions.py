#from basic_app.api_connection import league, get_week
from ff_espn_api import League
year = 2019
league_id = 1406490
swid = '{CC3929FE-4B90-497B-87D7-6283A951436F}'
espn_s2 = 'AECMpoZv%2FZF6G9Q1PEU9bnJD2Xf8FJwcFa8voarn81ZyGsMy8BzOpN8M6Wd9dLle3mHCQpW%2F0uQja23BYQagdA9H6tFSbtqGyyg%2BZs3m22Y%2FKNxo7os%2BBNSjX4bKa6UOSBlOph7KwtyMFBe654mVtR4inWzGYrTFVo2RIDk6ueNPFnz%2BDlKaxcQhRniwrEnXhprLfL78Gel1JetARL5lkiqGR2f%2BaPoxq%2Btfb8uj%2BzQAkMEkwJZaoWOUCPfxa7w%2FLa5GVnX5Ca%2F2ZqhFeysjWwOhYflDFnlItB1SKjpWPFtQ2w%3D%3D'
league = League(league_id, year, espn_s2, swid)

standings = league.standings()

def margin_and_loss(league):
    week = league.nfl_week
    obj = {'margin': [0, 0], 'big_loss': [0, 0]}
    for i in range(1, week):
        bs = league.box_scores(i)
        for game in bs:
            home_score = game.home_score
            away_score = game.away_score
            diff = home_score - away_score
            if diff > obj['margin'][0]:
                obj['margin'] = [diff, game.home_score, game.home_team.team_name, i]
            elif diff < -obj['margin'][0]:
                obj['margin'] = [abs(diff), game.away_score, game.away_team.team_name, i]
            if diff > 0 and away_score > obj['big_loss'][0]:
                obj['big_loss'] = [away_score, game.away_team.team_name, i]
            elif diff < 0 and home_score > obj['big_loss'][0]:
                obj['big_loss'] = [home_score, game.home_team.team_name, i]
    return obj

def get_standings(league):
    standings = league.standings()
    output = []
    for i in standings:
        x = [i.team_name, i.points_for, i.points_against, i.wins, i.losses, i.standing]
        output.append(x)
    return output


def week_scores(league):
    standings = league.standings()
    show_weeks = league.nfl_week - 1
    output = []
    for i in standings:
        adder = [i.team_name, i.scores[:show_weeks]]
        output.append(adder)
    return output


def get_trophies(league):
    standings = league.standings()
    m_and_l = margin_and_loss(league)
    margin = m_and_l['margin']
    bl = m_and_l["big_loss"]
    trophies = {
        'first': ['$375', standings[0].team_name],
        'second': ['$100', standings[1].team_name],
        'third': ['$50', standings[2].team_name],
        'season_winner': ['$25', standings[0].team_name],
        'skittish': ['$40', 'TBD'],
        'high_points': ['$25', league.top_scorer().team_name],
        'week10_16': ['$20', 'TBD'],
        'highest_loss': ['$10', bl[1], bl[0], bl[2]],
        'high_score': ['$10', league.top_scored_week()[0].team_name, league.top_scored_week()[1], 'TBD'],
        'margin': ['$10', margin[2], margin[1], margin[3]],
        'most_against': ['$10', league.most_points_against().team_name],
        'best_miss': ['$25', 'TBD']
    }
    leaders = {}
    for key, values in trophies.items():
        if values[1] in leaders:
            leaders[values[1]] += int(values[0][1:])
        elif values[1] not in leaders:
            leaders[values[1]] = int(values[0][1:])

    dollars = []
    for key, value in leaders.items():
        temp = [key, value]
        dollars.append(temp)
    output = {'trophies': trophies, 'dollars': dollars}
    return output


def skittish(league): # outputs dictionary with key=game week, value =[losing score, team name], along with a list of survivors

    week = league.nfl_week
    skitted = []
    weekly_dict = {}
    losers = []

    for w in range(1, week):
        matchups = league.box_scores(w)
        score = {}
        for i in matchups:
            ht = i.home_team.team_name
            hs = i.home_score
            if ht not in losers:
                score[ht] = hs
            at = i.away_team.team_name
            ascore = i.away_score
            if at not in losers:
                score[at] = ascore
        low_scorer = min(score.keys(), key=(lambda k: score[k]))
        losers.append(low_scorer)
        skit = [w, score.pop(low_scorer), low_scorer]
        skitted.append(skit)
        weekly_dict[w] = score
    survivors = list(weekly_dict[week-1].keys())

    return [skitted, survivors]
