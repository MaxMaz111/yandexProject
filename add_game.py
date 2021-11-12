from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QAbstractItemView

from database import DataBase
from db_manager import DataBaseManager


class AddGame(QMainWindow):
    def __init__(self, other, friend):
        uic.loadUi("addGameWindow.ui", other)
        super().__init__()
        other.allGamesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        other.pickedGamesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        other.addGamesToFriendButton.clicked.connect(other.add_games_to_friend)
        self.db_manager = DataBaseManager("my_db.sqlite", other)
        self.db = DataBase(other)
        other.allGamesTable.setColumnCount(1)
        other.allGamesTable.setRowCount(0)
        other.allGamesTable.setHorizontalHeaderLabels(['Все игры'])
        other.allGamesTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        other.pickedGamesTable.setColumnCount(1)
        other.pickedGamesTable.setRowCount(0)
        other.pickedGamesTable.setHorizontalHeaderLabels(['Игры друга'])
        other.pickedGamesTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        other.steamNameLabel.setText(friend.primary_key)
        other.friendDescText.setText(f'Описание друга: {friend.state["description"]}')
        other.returnBackButton.clicked.connect(other.return_back)
        right_table_rows_counter = 1
        for i in range(len(self.db.db["Games"])):
            for j in range(len(self.db.db["FriendsGames"])):
                if self.db.db["Games"][i].primary_key == self.db.db["FriendsGames"][j].get_state()[2]\
                        and friend.primary_key == self.db.db["FriendsGames"][j].get_state()[1]:
                    other.pickedGamesTable.setRowCount(right_table_rows_counter)
                    other.pickedGamesTable.setItem(right_table_rows_counter - 1, 0,
                                                   QTableWidgetItem(str(self.db.db["Games"][i])))
                    right_table_rows_counter += 1
        right_games_counter = 0
        left_games_counter = 1
        for i in range(len(self.db.db["Games"])):
            is_in_right_table = False
            for j in range(len(self.db.db["FriendsGames"])):
                if self.db.db["Games"][i].primary_key == self.db.db["FriendsGames"][j].get_state()[2] and \
                        friend.primary_key == self.db.db["FriendsGames"][j].get_state()[1]:
                    is_in_right_table = True
                    right_games_counter += 1
            if not is_in_right_table:
                other.allGamesTable.setRowCount(left_games_counter)
                other.allGamesTable.setItem(left_games_counter - 1, 0, QTableWidgetItem(str(self.db.db["Games"][i])))
                left_games_counter += 1
        other.allGamesTable.doubleClicked.connect(other.pick)
        other.pickedGamesTable.doubleClicked.connect(other.unpick)
