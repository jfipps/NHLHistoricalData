# Main function for The Stand
import NHLTeamNames as NHL
import NHLRoster as Roster
import NHLTeamStandings as Standings
import MenuProcessing as menu

# Gets user input for team name
def get_user_input():
    ny = 'New York'
    team_name = input("Enter in a team: ")
    if team_name.replace(' ', '').lower() in ny.replace(' ', '').lower():
        team_name = input("Rangers or Islanders? ")
        if team_name.lower() == 'rangers':
            return team_name
        elif team_name.lower() == 'islanders':
            return team_name
        else:
            return "Not in list"
    return team_name

# Process for getting league standings
def Standings_Choice():
    presort_teams = Standings.get_standings_data()
    sorted_teams = Standings.get_team_points(presort_teams)
    print(sorted_teams)
    Standings.display(sorted_teams)

# Process for getting info on specific team
def Team_Info_Choice():
    choice = get_user_input()
    print(f'This is your choice {choice}')
    if choice == 'Not in list':
        print(choice)
    else:
        teams = NHL.get_teams_data()
        teams_sorted = NHL.parse_and_sort(teams)

        stats = NHL.get_stats_data(choice, teams_sorted)

        if stats != "Not in list":
            print('------------------------------')
            team_season_standings = NHL.display_team_stats(stats)
            # This is grabbing team ID, use in URL to get player stats
            # statsapi.web.nhl.com/api/v1/teams/ID?hydrate=roster(person(stats(split=statsSingleSeason)))
            team_ID = team_season_standings[0][1]['id']
            roster_JSON = Roster.get_team_players(team_ID)
            roster_sorted = Roster.parse_and_sort_players(roster_JSON)
            print('------------------------------')
            Roster.display_roster(roster_sorted)
        else:
            print("Not in list")

# Menu for user, loops until done
def get_option():
    menu_choice = 1
    while menu_choice != 0:
        menu_choice = input("""Select from the following:
                                1) Display standings
                                2)Enter in team name for roster
                                0) Quit
                                Enter choice here: """)

        if int(menu_choice) == 1:
            Standings_Choice()
        elif int(menu_choice) == 2:
            Team_Info_Choice()
        elif int(menu_choice) == 0:
            break
        else:
            "Invalid choice"

get_option()
