"""
main.py
==============
"""

from flask import (
    Flask, render_template, request, jsonify, flash,
    redirect, session, url_for
)

from json import dumps, loads
import traceback

app = Flask(__name__, template_folder="./templates", static_folder="./static")
app.secret_key = b"elink_secret_key"

@app.route("/")
def index():
    return render_template(
        "pages/signup.html",
        context={}
    )

if __name__ == "__main__":
    app.run()
