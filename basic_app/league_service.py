from datetime import date
from operator import itemgetter
from basic_app.api_connection import get_league
from basic_app.api_functions import get_week
from basic_app.models import CurrentSeason, Rankings, Skittish, Player, PastSeasons
from basic_app.player_services import PlayerInfo



# note that from espn api: league.teams returns list of team objects. 
# each team.team_id is equal to db Player.player_id

class LeagueInfo:

    def __init__(self):
        self.league = get_league()
        self.year = CurrentSeason.objects.first().year
        self.players = {}
        self.matchups = []

    def load_players(self):
        for p in self.league.teams:
            oid = str(p.team_id)
            owner = PlayerInfo(id=p.team_id)
            self.players[oid] = owner.info()

    def load_matchups(self):
        match = self.league.scoreboard()
        for m in match:
            t = (m.home_team.team_id, m.away_team.team_id)
            self.matchups.append(t)

    def get_hybrid_standings(self):
        self.load_players()
        flat_players = list(self.players.values())
        hybrid_rank = sorted(flat_players, key=itemgetter('hybrid_wins', 'points_for'), reverse=True)
        return hybrid_rank

    def get_matchups(self):
        data = []
        self.load_matchups()
        self.load_players()

        for game in self.matchups:
            h = self.players.get(str(game[0]))
            a = self.players.get(str(game[1]))
            info = {'team1':h, 'team2':a}
            data.append(info)

        return data







    


