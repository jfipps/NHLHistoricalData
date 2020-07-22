from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QLabel, QWidget, QListWidgetItem, QListWidget, QComboBox
import sys, datetime, os
import NHLTeamStandings as TeamStandings
import RosterWindow as RosterWindow
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QRect, Qt

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.styleSheet = """
        QListWidget{
        background-color: rgba(255,255,255,0%);
        border: 0px;
        }
        
        QListWidget::item{padding-bottom: 5px;}        
        """
        self.title = "Team Standings"
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

        # Sets title at top of window
        titleLabel = QLabel("NHL Standings")
        titleLabel.setAlignment(Qt.AlignTop)
        titleLabel.setFont(QtGui.QFont("Ariel", 18, QtGui.QFont.Bold))
        self.hbox.addWidget(titleLabel)

        # Creates combo box for which season user would like to view
        self.yearStandingsCombo = QComboBox()
        self.fillComboBox()
        self.yearStandingsCombo.currentTextChanged.connect(self.comboChange)
        self.hbox.addWidget(self.yearStandingsCombo)
        self.vbox.addLayout(self.hbox)

        # Gets the current season's standings as default, will change on user action
        teamStandings = self.GetTeamStandings("http://statsapi.web.nhl.com/api/v1/standings")

        self.teamStandingsList = QListWidget()
        self.fillTeamList(teamStandings)

        # Button click action configuration
        self.teamStandingsList.itemClicked.connect(self.buttonClickEvent)
        self.teamStandingsList.setFont(QtGui.QFont("Ariel", 14))
        self.teamStandingsList.setResizeMode(True)
        self.teamStandingsList.setIconSize(QtCore.QSize(48, 48))

        self.vbox.addWidget(self.teamStandingsList)

        self.setStyleSheet(self.styleSheet)
        self.setLayout(self.vbox)

    # Send initial URL to NHLTeamStandings.py to get standings JSON data
    def GetTeamStandings(self, team_info_url):
        team_info_data = TeamStandings.get_json_data(team_info_url)
        presort_teams = TeamStandings.get_standings_data(team_info_data)
        return TeamStandings.get_team_points(presort_teams)

    # Fills QListWidget with standings
    def fillTeamList(self, teamStandings):
        self.teamStandingsList.clear()
        for team in teamStandings:
            item = QListWidgetItem(f'{team[0]} --- Points: {team[1]}')
            if os.path.isfile(f"TeamLogos\\{team[0]}.jpg"):
                item.setIcon(QtGui.QIcon(f"TeamLogos\\{team[0]}.jpg"))
            self.teamStandingsList.addItem(item)

    # Takes user to RosterWindow.py for team clicked on
    def buttonClickEvent(self, item):
        season = self.yearStandingsCombo.currentText().replace('-', '')
        team = str(item.text()).split(' -')[0]
        self.dialog = RosterWindow.TeamWindow(team, season)
        self.dialog.show()

    # Fills combo box with seasons to choose from
    def fillComboBox(self):
        currYear = datetime.datetime.today().year
        years = []
        for x in range(1920, currYear):
            years.append(str(x) + '-' + str(x + 1))
        years.reverse()
        for year in years:
            self.yearStandingsCombo.addItem(year)

    # Takes QComboBox text and appends to new URL for new team standings QListWidget
    def comboChange(self):
        season = self.yearStandingsCombo.currentText().replace('-', '')
        team_info_data = TeamStandings.get_json_data("http://statsapi.web.nhl.com/api/v1/standings?season=" + str(season))
        presort_teams = TeamStandings.get_standings_data(team_info_data)
        sort_teams = TeamStandings.get_team_points(presort_teams)
        self.fillTeamList(sort_teams)


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())