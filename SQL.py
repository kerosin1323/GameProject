import sqlite3


class Player:
    def __init__(self, name):
        self.name = name
        try:
            self.connect = sqlite3.connect('pyball.db')
            self.cursor = self.connect.cursor()
        except Exception:
            self.connect.close()
            Player(self.name)
        self.cursor.execute('INSERT INTO player(name) VALUES (?)', (self.name, ))
        self.connect.commit()
        if len(self.cursor.execute('SELECT * FROM againstBot WHERE name = ?', (name, )).fetchall()) == 0:
            self.cursor.execute('INSERT INTO againstBot(name) VALUES (?)', (name, ))
        self.connect.commit()


class AgainstBotDB:
    def __init__(self, name, result, goals1, goals2, stage):
        try:
            self.connect = sqlite3.connect('pyball.db')
            self.cursor = self.connect.cursor()
        except Exception:
            self.connect.close()
            AgainstBotDB(name, result, goals1, goals2, stage)
        self.cursor.execute('UPDATE againstBot SET matches = matches + 1, wins = wins + ?, draws = draws + ?, '
                            'loses = loses + ?, scored = scored + ?, missed = missed + ?, stage = ? WHERE name = ?',
                            (*result, goals1, goals2, stage, name))
        self.connect.commit()