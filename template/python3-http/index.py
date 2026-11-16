from flask import Flask, request, make_response
from waitress import serve
import os
from function import handler

app = Flask(__name__)

class Event:
    def __init__(self):
        self.body = request.get_data()
        self.headers = request.headers
        self.method = request.method
        self.query = request.args
        self.path = request.path

class Context:
    def __init__(self):
        self.hostname = os.getenv("HOSTNAME", "localhost")

def format_status_code(resp):
    if "statusCode" in resp:
        return resp["statusCode"]
    return 200

def format_body(resp):
    if "body" not in resp:
        return ""
    return resp["body"]

def format_headers(resp):
    if "headers" not in resp:
        return {}
    return resp["headers"]

def format_response(resp):
    if resp is None:
        return ("", 200)
    if isinstance(resp, dict):
        statusCode = format_status_code(resp)
        body = format_body(resp)
        headers = format_headers(resp)
        res = make_response(body, statusCode)
        for key, value in headers.items():
            res.headers[key] = value
        return res
    return resp

@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def main_route(path):
    event = Event()
    context = Context()
    resp = handler.handle(event, context)
    return format_response(resp)

if __name__ == "__main__":
    serve(app, host="127.0.0.1", port=5000)
