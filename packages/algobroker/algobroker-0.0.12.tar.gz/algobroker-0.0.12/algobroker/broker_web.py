#!/usr/bin/env python3
# http://flask.pocoo.org/snippets/116/

import zmq.green as zmq
from flask import Flask, send_from_directory, Response, request
import flask
import json

import algobroker
algobroker.set_zmq(zmq)

from io import StringIO
from gevent.queue import Queue
import sys
import time
from gevent.wsgi import WSGIServer
import gevent

subscriptions = []
app = Flask(__name__)


class BrokerWeb(algobroker.Broker):

    def __init__(self):
        algobroker.Broker.__init__(self, "broker_web")

    def process_data(self, data):
        self.info(data)
        if (data['cmd'] == "alert" and
                data["type"] == "web"):
            msg = {
                "id": "log",
                "level": "info",
                "msg": data['text']
            }
            for sub in subscriptions[:]:
                sub.put(msg)
        if(data['cmd'] == "send"):
            msg = data
            del msg['cmd']
            if id not in msg:
                msg['id'] = "log"
            for sub in subscriptions[:]:
                sub.put(msg)

if __name__ == "__main__":
    bw = BrokerWeb()
    g = gevent.Greenlet.spawn(bw.run)
    # Then visit http://localhost:5000 to subscribe
    # and send messages by visiting http://localhost:5000/publish


# SSE "protocol" is described here: http://mzl.la/UPFyxY
class ServerSentEvent(object):

    def __init__(self, data, event=None, id=None):
        self.data = json.dumps(data)
        self.event = event
        self.id = id
        self.desc_map = {
            self.data: "data",
            self.event: "event",
            self.id: "id"
        }

    def encode(self):
        if not self.data:
            return ""
        lines = ["%s: %s" % (v, k)
                 for k, v in self.desc_map.items() if k]
        return "%s\n\n" % "\n".join(lines)


@app.route("/angularjs")
def angularjs():
    return app.send_static_file('broker_web.html')


@app.route("/")
@app.route("/reactjs")
def reactjs():
    return app.send_static_file('broker_reactjs.html')


@app.route("/test-data")
def testdata():
    return flask.jsonify({"records": [{"Name": "foo",
                                       "Country": "bar"},
                                      {"Name": "foo1",
                                       "Country": "bar1"}]})


@app.route("/inject", methods=['GET', 'POST'])
def inject():
    algobroker.send(request.json)
    return "Done"

@app.route("/debug")
def debug():
    return "Currently %d subscriptions" % len(subscriptions)


@app.route("/publish-test")
def publish():
    msg = {
        "id": "log",
        "level": "info",
        "msg": str(time.time())
    }
    for sub in subscriptions[:]:
        sub.put(msg)
    return "OK"


@app.route("/subscribe")
def subscribe():
    def gen():
        q = Queue()
        subscriptions.append(q)
        try:
            while True:
                result = q.get()
                id = result['id']
                ev = ServerSentEvent(result, id)
                yield ev.encode()
        except GeneratorExit:  # Or maybe use flask signals
            subscriptions.remove(q)
    return Response(gen(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.debug = True
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
