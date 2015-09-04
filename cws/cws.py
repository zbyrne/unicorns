import sqlite3
import json
import time
from urlparse import urlparse, parse_qsl
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler


db = sqlite3.connect(":memory:")
cursor = db.cursor()
cursor.execute("CREATE TABLE clrs (uuid text, time real)")
db.commit()


def find_db_entry(uuid):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM clrs WHERE uuid='{0}'".format(uuid))
    return cursor.fetchone()


def update_db_entry(uuid):
    cursor = db.cursor()
    t = int(time.time())
    if find_db_entry(uuid) is None:
        cursor.execute("INSERT INTO clrs (uuid, time) VALUES ('{0}', '{1}')".format(uuid, t))
    else:
        cursor.execute("UPDATE clrs SET time='{1}' WHERE uuid='{0}'".format(uuid, t))
    db.commit()
    return t


class CwsRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        args = dict(parse_qsl(url.query))
        resp_dict = {}
        if 'uuid' in args:
            db_time = update_db_entry(args['uuid'])
            resp_dict['db_time'] = db_time
        if 'peer' in args:
            db_peer = find_db_entry(args['peer'])
            if db_peer is not None:
                resp_dict['peer_db_time'] = int(db_peer[1])
        resp = json.dumps(resp_dict)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-Length", str(len(resp)))
        self.end_headers()
        self.wfile.write(resp)


db = sqlite3.connect(":memory:")
cursor = db.cursor()
cursor.execute("CREATE TABLE clrs (uuid text, time real)")
db.commit()

server = HTTPServer(('localhost', 8080), CwsRequestHandler)
server.serve_forever()
