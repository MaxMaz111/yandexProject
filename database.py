from db_manager import DataBaseManager
from db_tuple import DBTuple

from dialog import Dialog


class DataBase:
    def __init__(self, window):
        self.window = window
        self.db_manager = DataBaseManager("my_db.sqlite", window)
        self.tables_name = self.db_manager.get_tables_name()
        self.db = {}
        for table_name in self.tables_name:
            table = self.db_manager.select(table_name, '*')
            self.db[table_name] = []
            for values in table:
                if values:
                    self.db[table_name].append(DBTuple(table_name, values, "None"))

    def add_DBTuple(self, db_tuple):
        is_in_table = False
        for t in self.db[db_tuple.table]:
            if (db_tuple.table == "FriendsGames"
                    and db_tuple.get_state()[1] == t.get_state()[1]
                    and db_tuple.get_state()[2] == t.get_state()[2]):
                is_in_table = True
                break
        if is_in_table:
            Dialog('Вы уже добавили эту игру другу')
        elif db_tuple.table == 'Friends' and not db_tuple.state['steam_name'] and not db_tuple.state["name"]:
            Dialog("Введите имя и ник друга")
        elif db_tuple.table == 'Friends' and not db_tuple.state['steam_name']:
            Dialog("Введите ник друга")
        elif db_tuple.table == 'Friends' and not db_tuple.state["name"]:
            Dialog("Введите имя друга")
        elif db_tuple.table == 'Games' and not db_tuple.state['name']:
            Dialog('Введите название игры')
        elif db_tuple.primary_key or db_tuple.primary_key == 0:
            self.db.get(db_tuple.table).append(db_tuple)
            self.upload_to_db()
        db_tuple.handling_type = "None"

    def upload_to_db(self):
        for table_name in self.tables_name:
            for db_tuple in self.db[table_name]:
                if db_tuple.handling_type == "insert":
                    self.db_manager.insert(table_name, db_tuple.get_fields_names(), db_tuple.get_state())
                elif db_tuple.handling_type == "update":
                    self.db_manager.update(table_name, db_tuple.get_fields_names(), db_tuple.get_state())
                elif db_tuple.handling_type == "delete":
                    self.db_manager.delete(table_name, db_tuple.get_fields_names(), db_tuple.get_state())
