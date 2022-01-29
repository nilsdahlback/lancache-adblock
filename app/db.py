import sqlite3

class Database:
    def __init__(self, **kwargs):
        self.db = kwargs.get('db')
        self.table = kwargs.get('table')

    def check_db(self):
        if self._db.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{}' '''.format(self._table)).fetchone()[0] == 0:
            self._db.execute(''' CREATE TABLE {} ( service CHAR(25) NOT NULL, domain VARCHAR(255) NOT NULL, last_update DATETIME, last_commit DATETIME )'''.format(self._table))
            self._db.commit()
            return True
        else:
            return False

    def check_update(self):
        return dict(self._db.execute(''' SELECT last_update from {} '''.format(self._table)).fetchone())['last_update']

    def check_commit(self):
        return dict(self._db.execute(''' SELECT last_commit from {} '''.format(self._table)).fetchone())['last_commit']

    def insert(self, parse):
        self._db.executemany('INSERT INTO {} VALUES (?, ?, ?, ?)'.format(self._table), parse)
        self._db.commit()

    def retrieve(self, ip):
        l = []
        r = self._db.execute(''' SELECT domain FROM {} '''.format(self._table))
        for i in r:
            l.append('{} {}'.format(ip, i[0]))
        return l

    def delete(self, timestamp):
        self._db.execute('DELETE FROM {} WHERE last_update={}'.format(self._table, timestamp))
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
