#!/usr/bin/python3
"""
endpoint will be to return the status of your API

"""

from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
import os
from api.v1.views import app_views

app = Flask('__name__')

app.register_blueprint(app_views, url_prefix='/api/v1')
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(exception):
    """close storage in case of teardown"""
    storage.close()


@app.errorhandler(404)
def handle_404_error(error):
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response

if os.getenv("HBNB_API_HOST"):
    host = os.getenv("HBNB_API_HOST")
else:
    host = "0.0.0.0"

if os.getenv("HBNB_API_PORT"):
    port = int(os.getenv("HBNB_API_PORT"))
else:
    port = 5000

if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True)
