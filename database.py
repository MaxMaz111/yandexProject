from db_manager import DataBaseManager
from entity import DBTuple


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
            if db_tuple.primary_key == t.primary_key or (db_tuple.table == "FriendsGames"
                                                         and db_tuple.get_state()[1] == t.get_state()[1]
                                                         and db_tuple.get_state()[2] == t.get_state()[2]):
                is_in_table = True

        if is_in_table:
            pass
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
