import sqlite3


class Player:
    """БД таблица с данными пользователя"""
    def __init__(self, name):
        self.name = name
        try:
            # подключение к БД
            self.connect = sqlite3.connect('pyball.db')
            self.cursor = self.connect.cursor()
        except Exception:
            self.connect.close()
            Player(self.name)
        self.cursor.execute('INSERT INTO player(name) VALUES (?)', (self.name,))
        self.connect.commit()


class AgainstBotDB:
    """Данные пользователя в режиме Против бота"""
    def __init__(self, name):
        self.name = name
        try:
            # подключение к БД
            self.connect = sqlite3.connect('pyball.db')
            self.cursor = self.connect.cursor()
        except Exception:
            self.connect.close()
            AgainstBotDB(self.name)
        if len(self.cursor.execute('SELECT * FROM againstBot WHERE name = ?', (self.name,)).fetchall()) == 0:
            self.cursor.execute('INSERT INTO againstBot(name) VALUES (?)', (self.name,))
            self.connect.commit()

    def append(self, result, goals1, goals2, stage, country1, country2):
        # добавление результата игры
        self.cursor.execute('UPDATE againstBot SET matches = matches + 1, wins = wins + ?, draws = draws + ?, '
                            'loses = loses + ?, scored = scored + ?, missed = missed + ?, stage = ?, cleansheets = cleansheets + ?'
                            'WHERE name = ?', (*result, goals1, goals2, stage, goals2 == 0, self.name))
        self.connect.commit()
        self.cursor.execute('INSERT INTO matches(name, country1, country2, goals1, goals2) VALUES (?, ?, ?, ?, ?)',
                            (self.name, country1, country2, goals1, goals2))
        self.connect.commit()

    def get_all(self):
        # получение статистики
        result = self.cursor.execute('SELECT matches, wins, draws, loses, scored, missed, cleansheets FROM againstBot '
                                     'WHERE name = ?', (self.name,)).fetchall()
        return result if result else [(0, 0, 0, 0, 0, 0, 0)]


class OnlineDB:
    """Данные пользователя в режиме Онлайн"""
    def __init__(self, name):
        self.name = name
        try:
            # подключение к БД
            self.connect = sqlite3.connect('pyball.db')
            self.cursor = self.connect.cursor()
        except Exception:
            self.connect.close()
            OnlineDB(self.name)

    def append(self, result, goals1, goals2):
        # добавление статистики матча
        if len(self.cursor.execute('SELECT * FROM online WHERE name = ?', (self.name,)).fetchall()) == 0:
            self.cursor.execute('INSERT INTO online(name) VALUES (?)', (self.name,))
            self.connect.commit()
        self.cursor.execute('UPDATE online SET matches = matches + 1, wins = wins + ?, draws = draws + ?, '
                            'loses = loses + ?, scored = scored + ?, missed = missed + ? WHERE name = ?',
                            (*result, goals1, goals2, self.name))
        self.connect.commit()

    def get_all(self):
        # получение статистики
        result = self.cursor.execute('SELECT matches, wins, draws, loses, scored, missed, cleansheets FROM online '
                                     'WHERE name = ?', (self.name,)).fetchall()
        return result if result else [(0, 0, 0, 0, 0, 0, 0)]
