import json
import ssl
import urllib.request

# Sort teams by id
def SortTeams(val):
    return val['person']['primaryPosition']['type']

# Sort players by name:
def SortPlayers(val):
    return val['person']['primaryPosition']['name']
# Parsing team info json link and sets roster info into list
def get_team_players(team_ID, season):
    team_info_url = "http://statsapi.web.nhl.com/api/v1/teams/" + str(team_ID) + "?hydrate=roster(person(stats(splits=statsSingleSeason)))&season=" + str(season)
    response = urllib.request.urlopen(team_info_url)
    team_info_data = json.loads(response.read())
    return team_info_data

# Parses info from teams list into roster list, then sorts by position
def parse_and_sort_players(team_info_data):
    teams = []
    roster_count = 0
    for team in team_info_data['teams']:
        while roster_count < (len(team['roster']['roster']) - 1):
            teams.append(team['roster']['roster'][roster_count])
            roster_count += 1
    teams.sort(key=SortTeams)
    return teams

# Returns roster for team selected in main window. Will leave out any players with no stats recorded.
def display_roster(players):
    playerList = []
    for player in players:
        name = player['person']['fullName']
        position = player['person']['primaryPosition']['type']
        # Appends players to list. Differentiates between goalie and non goalie as data structure is different
        if position != 'Goalie':
            # Checks if player has current stats, ignores those with 0 points
            if len(player['person']['stats'][0]['splits']) > 0:
                goals = player['person']['stats'][0]['splits'][0]['stat']['goals']
                assists = player['person']['stats'][0]['splits'][0]['stat']['assists']
                points = goals + assists
                if points > 0:
                    playerList.append(f"{name} --- {position} --- G:{goals} A:{assists} P:{points}")
        else:
            if len(player['person']['stats'][0]['splits']) > 0:
                wins = player['person']['stats'][0]['splits'][0]['stat']['wins']
                losses = player['person']['stats'][0]['splits'][0]['stat']['losses']
                savePercentage = player['person']['stats'][0]['splits'][0]['stat']['savePercentage']
                playerList.append(f"{name} --- {position} --- W:{wins} L:{losses} SP:{savePercentage}")
    return playerList

