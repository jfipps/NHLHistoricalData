from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QLabel, QWidget, QLineEdit, QPushButton, QInputDialog, QMessageBox, QListWidget, QComboBox, QSizePolicy
import sys
from PyQt5 import QtGui, Qt
from PyQt5.QtCore import QRect
import NHLTeamNames as NHL
import NHLRoster as Roster
import NHLTeamStandings as Standings

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "Roster"
        self.left = 500
        self.top = 500
        self.width = 900
        self.height = 850

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.InitUI()

        self.show()

    def InitUI(self):
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()

        # Hbox initialization
        label = QLabel("Select Team: ")
        self.hbox.addWidget(label)
        self.combo = QComboBox()
        self.combo.setSizePolicy(QSizePolicy.Expanding, 0)
        self.fillCombo()
        self.combo.currentTextChanged.connect(self.displayTeamInfo)
        self.hbox.addWidget(self.combo)
        self.vbox.addLayout(self.hbox)

        #Vbox initialization
        # Team standings and roster initialization
        self.teamStanding = QLabel("")
        self.vbox.addWidget(self.teamStanding)
        self.teamRosterList = QListWidget()
        self.teamRosterList.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.vbox.addWidget(self.teamRosterList)

        self.vbox.addStretch()
        self.setLayout(self.vbox)

    def displayTeamInfo(self):
        # Gets user choice from the combo box dropdown
        choice = self.combo.currentText()
        self.teamRosterList.clear()
        teams = NHL.get_teams_data()
        teams_sorted = NHL.parse_and_sort(teams)

        stats = NHL.get_stats_data(choice, teams_sorted)

        if stats != "Not in list":
            team_season_standings = NHL.display_team_stats(stats)
            for team in team_season_standings:
                self.teamStanding.setText(
                    f"Team: {team[1]['name']} -- Record: W-{team[0]['wins']} L-{team[0]['losses']} OT-{team[0]['ot']} Pts-{team[0]['pts']}")
            # This is grabbing team ID, use in URL to get player stats
            # statsapi.web.nhl.com/api/v1/teams/ID?hydrate=roster(person(stats(split=statsSingleSeason)))
            team_ID = team_season_standings[0][1]['id']
            roster_JSON = Roster.get_team_players(team_ID)
            roster_sorted = Roster.parse_and_sort_players(roster_JSON)
            players = Roster.display_roster(roster_sorted)
            for player in players:
                self.teamRosterList.addItem(player)
        else:
            print("Not in list")

    def fillCombo(self):
        self.combo.addItem("---Select---")
        self.combo.addItem("Anaheim Ducks")
        self.combo.addItem("Arizona Coyotes")
        self.combo.addItem("Boston Bruins")
        self.combo.addItem("Buffalo Sabres")
        self.combo.addItem("Calgary Flames")
        self.combo.addItem("Carolina Hurricanes")
        self.combo.addItem("Chicago Blackhawks")
        self.combo.addItem("Colorado Avalanche")
        self.combo.addItem("Columbus Blue Jackets")
        self.combo.addItem("Dallas Stars")
        self.combo.addItem("Detroit Red Wings")
        self.combo.addItem("Edmonton Oilers")
        self.combo.addItem("Florida Panthers")
        self.combo.addItem("Los Angeles Kings")
        self.combo.addItem("Minnesota Wild")
        self.combo.addItem("Montreal Canadiens")
        self.combo.addItem("Nashville Predators")
        self.combo.addItem("New Jersey Devils")
        self.combo.addItem("New York Islanders")
        self.combo.addItem("New York Rangers")
        self.combo.addItem("Ottawa Senators")
        self.combo.addItem("Philadelphia Flyers")
        self.combo.addItem("Pittsburgh Penguins")
        self.combo.addItem("St. Louis Blues")
        self.combo.addItem("San Jose Sharks")
        self.combo.addItem("Tampa Bay Lightning")
        self.combo.addItem("Toronto Maple Leafs")
        self.combo.addItem("Vancouver Canucks")
        self.combo.addItem("Vegas Golden Knights")
        self.combo.addItem("Washington Capitals")
        self.combo.addItem("Winnipeg Jets")

if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())