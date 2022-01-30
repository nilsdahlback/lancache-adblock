from threading import Thread, Event

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
        # Since anonymous API calls to Github are rate limited at 60/h we only do 6 to ensure we don't exceed it.
        e.wait(600)
        # Check for git commit updates to the cache domain json file.
        if  d.check_update() < c.check_tm(CONFIG['repo']):
            d.insert(c.parse())
            # Remove older unused parses to reduce database size.
            d.clean()

if __name__ == '__main__':
    e = Event()
    thread = Thread(target=cache_thread, args=(e,), daemon=True)
    thread.start()
    app.run(debug=True)
