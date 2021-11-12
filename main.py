import sys

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QAbstractItemView

from add_game import AddGame
from database import DataBase
from entity import DBTuple


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainWindow.ui', self)
        self.db = DataBase(self)
        self.addGameButton.clicked.connect(self.add_game)
        self.addFriendButton.clicked.connect(self.add_friend)
        self.gamesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.friendsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.gamesTable.doubleClicked.connect(self.set_players)
        self.friendsTable.doubleClicked.connect(self.set_games)
        self.refreshTables()

    def refreshTables(self):
        self.gamesTable.setColumnCount(1)
        self.friendsTable.setColumnCount(1)
        games_res = self.db.db["Games"]
        friends_res = self.db.db["Friends"]
        self.gamesTable.setHorizontalHeaderLabels(['Название игры'])
        self.friendsTable.setHorizontalHeaderLabels(['Ник'])
        self.gamesTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.friendsTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.gamesTable.setRowCount(len(games_res))
        self.friendsTable.setRowCount(len(friends_res))
        for i in range(len(friends_res)):
            self.friendsTable.setItem(i, 0, QTableWidgetItem(str(friends_res[i])))
        for i in range(len(games_res)):
            self.gamesTable.setItem(i, 0, QTableWidgetItem(str(games_res[i])))

    def add_game(self):
        self.stateLabel.setText('')
        name = self.gameNameLine.text()
        rating = self.gameRatingSpinBox.value()
        url = self.gameURLLine.text()
        desc = self.gameDescLine.text()
        self.db.add_DBTuple(DBTuple('Games', (name, rating, url, desc)))
        self.gameNameLine.setText('')
        self.gameRatingSpinBox.setValue(0)
        self.gameURLLine.setText('')
        self.gameDescLine.setText('')
        self.refreshTables()

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def set_games(self, index):
        friend = None
        for t in self.db.db["Friends"]:
            if index.data() == t.primary_key:
                friend = t
        AddGame(self, friend)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def set_players(self, i):
        print(i.row())

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def pick(self, i):
        self.pickedGamesTable.setRowCount(self.pickedGamesTable.rowCount() + 1)
        self.pickedGamesTable.setItem(self.pickedGamesTable.rowCount() - 1, 0, QTableWidgetItem(i.data()))
        self.allGamesTable.removeRow(i.row())

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def unpick(self, i):
        self.allGamesTable.setRowCount(self.allGamesTable.rowCount() + 1)
        self.allGamesTable.setItem(self.allGamesTable.rowCount() - 1, 0, QTableWidgetItem(i.data()))
        self.pickedGamesTable.removeRow(i.row())

    def add_friend(self):
        self.stateLabel.setText('')
        nick = self.friendNickLine.text()
        name = self.friendNameLine.text()
        desc = self.friendDescLine.text()
        self.db.add_DBTuple(DBTuple('Friends', (nick, name, desc)))
        self.friendNickLine.setText('')
        self.friendNameLine.setText('')
        self.friendDescLine.setText('')
        self.refreshTables()

    def return_back(self):
        uic.loadUi('mainWindow.ui', self)
        self.db = DataBase(self)
        self.addGameButton.clicked.connect(self.add_game)
        self.addFriendButton.clicked.connect(self.add_friend)
        self.gamesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.friendsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.gamesTable.doubleClicked.connect(self.set_players)
        self.friendsTable.doubleClicked.connect(self.set_games)
        self.refreshTables()

    def add_games_to_friend(self):
        friend = self.steamNameLabel.text()
        for i in range(self.pickedGamesTable.rowCount()):
            self.db.add_DBTuple(DBTuple("FriendsGames", (len(self.db.db["FriendsGames"]),
                                                         friend, self.pickedGamesTable.item(i, 0).data(0))))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
