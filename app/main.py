from flask import Flask, request

from .db import Database
from .config import CONFIG

app = Flask(__name__)

@app.route('/')
def index():
    q = request.args
    if not q.get('ip'):
        return 'You need to set which IP adress you would like to redirect DNS traffic to.<br/>Example: /?ip=<b>&lt;ip&gt;</b>', 200

    d = Database(db=CONFIG['db'], table=CONFIG['table'])
    r = "\n".join(d.retrieve(q.get('ip')))
    return r, 200, {'Content-Type': 'text/plain; charset=utf-8'}
