from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QLabel, QWidget, QLineEdit, QPushButton, QInputDialog, QMessageBox, QListWidget, QComboBox, QSizePolicy
import sys, os
from PyQt5 import QtGui, Qt, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect
import NHLTeamNames as NHLTeams
import NHLRoster as Roster

class TeamWindow(QWidget):
    def __init__(self, teamName, season):
        super().__init__()
        self.teamChoice = teamName
        self.season = season
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

        # Sets label at top of window to team name
        # label.setFont(QtGui.QFont("Ariel", 18, QtGui.QFont.Bold))
        if os.path.isfile(f"TeamLogos\\{self.teamChoice}.jpg"):
            teamLogo = QLabel(str(self.teamChoice))
            pixmap = QPixmap(f"TeamLogos\\{self.teamChoice}.jpg")
            teamLogo.setMaximumWidth(pixmap.width())
            teamLogo.setPixmap(pixmap)
            self.hbox.addWidget(teamLogo)
        label = QLabel(self.teamChoice)
        label.setFont(QtGui.QFont("Ariel", 18, QtGui.QFont.Bold))
        self.hbox.addWidget(label)
        self.vbox.addLayout(self.hbox)

        # Label for teams standing for the season chosen in TeamStandingsWindow
        self.teamStanding = QLabel("")
        self.vbox.addWidget(self.teamStanding)

        # Gathers list of the team's roster for that season. Will be displayed in order of position
        self.teamRosterList = QListWidget()
        self.displayTeamInfo(self.teamChoice, self.season)
        self.teamRosterList.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.teamRosterList.setFont(QtGui.QFont("Ariel", 14))
        self.teamRosterList.setResizeMode(True)
        self.setStyleSheet("""QListWidget{background-color: rgba(255,255,255,0%); border: 0px}""")
        self.vbox.addWidget(self.teamRosterList)

        self.setLayout(self.vbox)

    # Queries API for season roster and stats for the players for a given team
    # Also gets team standing for that season
    def displayTeamInfo(self, teamChoice, season):
        self.teamRosterList.clear()
        teams = NHLTeams.get_teams_data(season)
        teams_sorted = NHLTeams.parse_and_sort(teams)
        stats = NHLTeams.get_stats_data(teamChoice, teams_sorted, season)
        team_season_standings = NHLTeams.display_team_stats(stats)
        for team in team_season_standings:
            self.teamStanding.setText(
                f"Record: W-{team[0]['wins']} L-{team[0]['losses']} OT-{team[0]['ot']} Pts-{team[0]['pts']}")
            self.teamStanding.setFont(QtGui.QFont("Ariel", 10, QtGui.QFont.Bold))
        team_ID = team_season_standings[0][1]['id']
        roster_JSON = Roster.get_team_players(team_ID, season)
        roster_sorted = Roster.parse_and_sort_players(roster_JSON)
        players = Roster.display_roster(roster_sorted)
        for player in players:
            self.teamRosterList.addItem(player)

if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = TeamWindow()
    sys.exit(App.exec())