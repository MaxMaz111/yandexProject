class DBTuple:
    def __init__(self, table, values, handling_type="insert"):
        self.primary_key = values[0]
        self.state = {}
        self.table = table
        self.handling_type = handling_type
        for i in range(len(values)):
            self.state[self.get_fields_names()[i]] = values[i]

    def change(self, values):
        for i in range(len(values)):
            self.state[self.get_fields_names()[i]] = values[i]

    def get_state(self):
        return tuple([self.state[i] for i in self.get_fields_names()])

    def __str__(self):
        return str(self.primary_key)

    def __repr__(self):
        return str(self.primary_key)

    def get_fields_names(self):
        if self.table == 'Friends':
            return "steam_name", "name", "description"
        elif self.table == 'Games':
            return "name", "rating", "url", "description"
        elif self.table == 'FriendsGames':
            return "id", "steam_name", "game_name"
