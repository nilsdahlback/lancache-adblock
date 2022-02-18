import sqlite3


class Database:
    def __init__(self, **kwargs):
        self.db = kwargs.get('db')
        self.table = kwargs.get('table')

    def check_db(self):
        db_query = self._db.execute(
                ''' SELECT count(name) FROM sqlite_master \
                        WHERE type='table' AND name='{}' '''.format(
                            self._table))
        if db_query.fetchone()[0] == 0:
            self._db.execute(
                ''' CREATE TABLE {} ( service CHAR(25) NOT NULL, \
                        domain VARCHAR(255) NOT NULL, last_commit DATETIME ) \
                        '''.format(self._table))
            self._db.commit()
            return True
        else:
            return False

    def check_update(self):
        return self._db.execute('SELECT last_commit from {}'.format(
            self._table)).fetchone()[0]

    def insert(self, parse):
        self._db.executemany('INSERT INTO {} VALUES (?, ?, ?)'.format(
            self._table), parse)
        self._db.commit()

    def retrieve(self, ip):
        dns_list = []
        res = self._db.execute('SELECT domain FROM {}'.format(self._table))
        for i in res:
            dns_list.append('{} {}'.format(ip, i[0]))
        return dns_list

    def clean(self):
        r = self._db.execute(
                ''' SELECT DISTINCT COUNT(DISTINCT last_commit), last_commit \
                        FROM {} ORDER BY last_commit ASC '''.format(
                            self._table)).fetchone()
        if r[0] >= 3:
            self._db.execute('DELETE FROM {} WHERE last_commit=?'.format(
                self._table), (r[1],))
            self._db.commit()

    @property
    def db(self): return self._db

    @db.setter
    def db(self, file):
        self._db = sqlite3.connect(file)
        self._db.row_factory = sqlite3.Row

    @db.deleter
    def db(self): self.close()

    @property
    def table(self): return self._table

    @table.setter
    def table(self, t):
        self._table = t

    @table.deleter
    def table(self):
        del self._table

    def close(self):
        self._db.close()
        del self._db
