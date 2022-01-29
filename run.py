from threading import Thread, Event
from datetime import datetime, timedelta

from app.main import app
from app.cache import Cache
from app.db import Database
from app.config import CONFIG

def cache_thread(e):
    d = Database(db=CONFIG['db'], table=CONFIG['table'])
    c = Cache(repo=CONFIG['repo'], file=CONFIG['file'])
    # Check if table exists, if not create it and fill it.
    if d.check_db():
        d.insert(c.parse())
    while True:
        # Check if 24 hours have passed since last update check.
        if d.check_update() <= datetime.strftime(datetime.now()-timedelta(days=1), '%Y-%m-%d %H:%M:%S.%f'):
            commit = d.check_commit()
            if  commit <= c.check_tm(cache_repo):
                d.insert(c.parse())
                d.delete(commit)
        e.wait(600)

if __name__ == '__main__':
    e = Event()
    thread = Thread(target=cache_thread, args=(e,), daemon=True)
    thread.start()
    app.run(debug=False)
