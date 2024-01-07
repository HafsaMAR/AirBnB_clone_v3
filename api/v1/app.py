#!/usr/bin/python3
""""""
from flask import Flask, Blueprint
from models import storage
import os
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

@app.teardown_appcontext
def close_storage(exception):
    storage.close()

# if os.getenv("HBNB_API_HOST"):
#     host = "HBNB_API_HOST"
# else:
#     host = '0.0.0.0'

# if os.getenv("HBNB_API_PORT"):
#     port = "HBNB_API_PORT"
# else:
#     port = 5000

if __name__ == '__main__':
    host = os.getenv("HBNB_API_HOST", '0.0.0.0')
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)