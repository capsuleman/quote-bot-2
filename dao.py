import sqlite3


class DAO():

    def __init__(self):

        self.connexion = sqlite3.connect('quote.db')

        # Returns a query as a dict and not a tuple
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
        self.connexion.row_factory = dict_factory

        c = self.connexion.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS quotes (quote TEXT, author TEXT)')
        c.close()

    def add_quote(self, quote, author):
        c = self.connexion.cursor()
        c.execute(
            'INSERT INTO quotes (quote, author) VALUES (?, ?)',
            [quote, author]
        )
        self.connexion.commit()
        c.close()

    def get_random_quote(self, n):
        c = self.connexion.cursor()
        c.execute(
            'SELECT * FROM quotes ORDER BY RANDOM() LIMIT ?',
            [n]
        )
        quotes = c.fetchall()
        print(quotes)
        c.close()

    def get_last_quotes(self, n):
        c = self.connexion.cursor()
        c.execute(
            'SELECT * FROM quotes ORDER BY rowid DESC LIMIT ?',
            [n]
        )
        quotes = c.fetchall()
        print(quotes)
        c.close()

    def search_quote(self, keyword):
        keyword_with_wildcart = '%' + keyword + '%'
        c = self.connexion.cursor()
        c.execute(
            'SELECT * FROM quotes WHERE quote LIKE ? OR author LIKE ?',
            [keyword_with_wildcart, keyword_with_wildcart]
        )
        quotes = c.fetchall()
        print(quotes)
        c.close()
