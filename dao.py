import sqlite3


class DAO():

    def __init__(self):

        self.connexion = sqlite3.connect('quote.db', check_same_thread=False)

        # Returns a query as a dict and not a tuple
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
        self.connexion.row_factory = dict_factory

        c = self.connexion.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS quotes (content TEXT, author TEXT)')
        c.close()

    def add_quote(self, content, author):
        c = self.connexion.cursor()
        c.execute(
            'INSERT INTO quotes (content, author) VALUES (?, ?)',
            [content, author]
        )
        self.connexion.commit()
        c.close()

    def get_random_quotes(self, n):
        c = self.connexion.cursor()
        c.execute(
            'SELECT * FROM quotes ORDER BY RANDOM() LIMIT ?',
            [n]
        )
        quotes = c.fetchall()
        c.close()
        return quotes

    def get_last_quotes(self, n):
        c = self.connexion.cursor()
        c.execute(
            'SELECT * FROM quotes ORDER BY rowid DESC LIMIT ?',
            [n]
        )
        quotes = c.fetchall()
        c.close()
        return quotes

    def search_quotes(self, keyword):
        keyword_with_wildcart = '%' + keyword + '%'
        c = self.connexion.cursor()
        c.execute(
            'SELECT * FROM quotes WHERE content LIKE ? OR author LIKE ?',
            [keyword_with_wildcart, keyword_with_wildcart]
        )
        quotes = c.fetchall()
        c.close()
        return quotes
