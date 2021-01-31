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
        "pages/index.html",
        context={}
    )

@app.route("/signup")
def signup():
    return render_template(
        "pages/signup.html",
        context={}
    )

@app.route("/profile")
def profile():
    return render_template(
        "pages/profile.html",
        context={
            'full_name': 'Bob Jones',
            'personal_website': 'bobjones.com',
            'picture_src': 'https://cdn.pixabay.com/photo/2021/01/06/21/50/couple-5895728_960_720.jpg',
            'connections': {
                'User One': 'userone.com',
                'User Two': 'usertwo.com',
                'User Three': 'userthree.com'
                }
            }
    )

@app.route("/customize")
def customize():
    return render_template(
        "pages/customize.html",
        context={
            'full_name': 'Bob Jones',
            'email': 'hi@bobjones.com',
            'picture_src': 'https://cdn.pixabay.com/photo/2021/01/06/21/50/couple-5895728_960_720.jpg',
            'personal_website': 'bobjones.com',
            'theme': 'Light'
        }
    )

@app.route("/widget")
def widget():
    return render_template(
        "pages/widget.html",
        context={}
    )

if __name__ == "__main__":
    app.run()
