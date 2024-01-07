#!/usr/bin/python3
"""Define routes of blueprint"""
from flask import Flask, jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False, methods=["GET"])
def status():
    return jsonify({"status": 'OK'})
