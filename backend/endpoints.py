import json

from flask import Flask, request, jsonify
from flask.logging import create_logger

APP = Flask(__name__)
LOG = create_logger(APP)


@APP.route("/run", methods=["POST"])
def run():
    if request.method == "POST":
        # Extract Data
        data = json.loads(request.data)
        cas_input = data["input"]

        # TODO: Impliement CAS
        cas_output = cas_input
        error = ""

        response = jsonify({"output": cas_output, "error": error})
        response.headers.add("Access-Control-Allow-Origin", "*")

        return response
    else:
        LOG.error("This should be a POST request")
