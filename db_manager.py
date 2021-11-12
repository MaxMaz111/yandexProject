import sqlite3


class DataBaseManager:
    def __init__(self, database, window):
        self.con = sqlite3.connect(database)
        self.window = window

    def execute(self, query, has_db_changes=False):
        try:
            if has_db_changes:
                self.con.cursor().execute(query)
                self.con.commit()
            else:
                return self.con.cursor().execute(query).fetchall()
        except sqlite3.OperationalError:
            self.window.stateLabel.setText("Ошибка выполнения запроса в бд")

    def select(self, table, *fields, condition=''):
        if condition:
            return [list(i) for i in self.execute(f"SELECT {', '.join(list(fields))} FROM {table} WHERE ")]
        return [list(i) for i in self.execute(f"SELECT {', '.join(list(fields))} FROM {table}")]

    def get_tables_name(self):
        return [i[0] for i in self.execute("SELECT name FROM sqlite_master WHERE type='table'")[1::]]

    def insert(self, table, field_names, values):
        self.execute(f"INSERT INTO {table}{field_names} VALUES {values}", True)

    def update(self, table, field, value):
        self.execute(f"UPDATE {table} SET {field} = '{value}' ", True)

    def delete(self, table, field, value):
        self.execute(f"DELETE FROM {table} WHERE {field}={value}", True)
