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
from passlib.hash import sha256_crypt

from src import datastax

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

@app.route("/signup_filled", methods=["POST"])
def login_or_register():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    if "signin" in request.form:
        if datastax.has_account(username):
            if datastax.check_credentials(username, password):
                session["username"] = username
                return render_template(
                    "pages/signed_up.html",
                    context={"username":username}
                )
    if "register" in request.form:
        if datastax.username_free(username):
            datastax.make_account(username, password)
            session["username"] = username
            return render_template(
                "pages/signed_up.html",
                context={"username":username}
            )
    flash("Invalid credientials.")
    return redirect(url_for('signup_login'))

@app.route("/set_website", methods=["POST"])
def set_website():
    assert "username" in session, "Username not in session!"
    website = request.form.get("website", "https://www.google.com")
    datastax.set_website(session["username"], website)

@app.route("/get_connections", methods=["POST"])
def get_connections():
    username = request.json.get("username", "")
    if not has_account(username):
        return jsonify({})
    connections = {}
    for user in datastax.get_connections(username):
        connections[user] = datastax.get_website(user)
    return jsonify(connections)

@app.route("/change_connection", methods=["POST"])
def change_connection():
    username = request.json.get("username1", "")
    password = request.json.get("username2", "")
    other_user = request.json.get("other_user", "")
    if datastax.check_credentials(username, password):
        datastax.change_connection(username, other_user)
        return jsonify({"worked": True})
    return jsonify({"worked": False})

if __name__ == "__main__":
    app.run()
