import json

from flask import Flask, request, jsonify, abort
from flask.logging import create_logger

from session_handler import create_new_session, load_state, save_state

APP = Flask(__name__)
LOG = create_logger(APP)


@APP.route("/new-session", methods=["POST"])
def new_session():
    if request.method == "POST":

        session_id = create_new_session()

        response = jsonify({"id": session_id})
        response.headers.add("Access-Control-Allow-Origin", "*")

        return response
    else:
        LOG.error("This should be a POST request")


@APP.route("/run", methods=["POST"])
def run():
    if request.method == "POST":
        # Extract Data
        data = json.loads(request.data)
        cas_input = data["input"]

        # TODO: Impliement CAS
        cas_output = cas_input
        error = False

        response = jsonify({"output": cas_output, "error": error})
        response.headers.add("Access-Control-Allow-Origin", "*")

        return response
    else:
        LOG.error("This should be a POST request")
