import json

from flask import Flask, request, jsonify, abort
from flask.logging import create_logger

from session_handler import create_session, load_session_file, save_session_file

APP = Flask(__name__)
LOG = create_logger(APP)


@APP.route("/create-session", methods=["POST"])
def create():
    if request.method == "POST":

        session_id = create_session()

        response = jsonify({"id": session_id})
        response.headers.add("Access-Control-Allow-Origin", "*")

        return response
    else:
        LOG.error("This should be a POST request")


@APP.route("/get-history", methods=["POST"])
def get_history():
    if request.method == "POST":
        # Extract Data
        data = json.loads(request.data)
        id = data["id"]

        history = load_session_file(id, "history.pkl")

        response = jsonify({"history": history})
        response.headers.add("Access-Control-Allow-Origin", "*")

        return response
    else:
        LOG.error("This should be a POST request")


@APP.route("/update-history", methods=["POST"])
def update_history():
    if request.method == "POST":
        # Extract Data
        data = json.loads(request.data)
        id = data["id"]
        calculation = data["calculation"]

        history = load_session_file(id, "history.pkl")
        history.append(calculation)
        save_session_file(id, history, "history.pkl")

        response = jsonify({"success": True})
        response.headers.add("Access-Control-Allow-Origin", "*")

        return response
    else:
        LOG.error("This should be a POST request")


@APP.route("/run", methods=["POST"])
def run():
    if request.method == "POST":
        # Extract Data
        data = json.loads(request.data)
        id = data["id"]
        cas_input = data["input"]

        # TODO: Impliement CAS
        state = load_session_file(id, "state.pkl")
        cas_output = cas_input
        error = False

        response = jsonify({"output": cas_output, "error": error})
        response.headers.add("Access-Control-Allow-Origin", "*")

        return response
    else:
        LOG.error("This should be a POST request")
