from flask import Flask, redirect
from os import environ
from googleapiclient import discovery
import json


app = Flask(__name__)


@app.route("/api/<message>")
def api_message(message: str = ""):
    API_KEY = environ["PERSPECTIVE_KEY"]

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=API_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": message},
        "requestedAttributes": {"TOXICITY": {}},
    }

    response = client.comments().analyze(body=analyze_request).execute()
    print(json.dumps(response, indent=4))

    return response.json()


@app.route("/")
@app.route("/<text>")
def home(text: str = None):
    return redirect("https://dillonb07.github.io/toxicity-checker")


app.run(host="0.0.0.0", port=8080)
