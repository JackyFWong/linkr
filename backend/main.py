"""
main.py
=======
"""

from flask import (
    Flask, render_template, request, jsonify, flash,
    redirect, session, url_for
)
from flask_cors import CORS, cross_origin

from json import dumps, loads
import traceback
from passlib.hash import sha256_crypt

from src import datastax

app = Flask(__name__, template_folder="./templates", static_folder="./static")
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)
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
    username = session["username"]
    conns = {user:datastax.get_website(username) for user in datastax.get_connections(username)}
    return render_template(
        "pages/profile.html",
        context={
            'full_name': username,
            'personal_website': datastax.get_website(username),
            'picture_src': datastax.get_image(username),
            'connections': conns,
        }
    )

@app.route("/customize")
def customize():
    username = session["username"]
    conns = {user:datastax.get_website(username) for user in datastax.get_connections(username)}
    return render_template(
        "pages/customize.html",
        context={
            'full_name': username,
            'personal_website': datastax.get_website(username),
            'picture_src': datastax.get_image(username),
            'connections': conns,
            "email": datastax.get_email(username),
        }
    )

@app.route("/update_customization", methods=["POST"])
def update_customization():
    username = session["username"]
    print(request.form)
    if "email" in request.form:
        if request.form["email"] != "":
            datastax.set_email(username, request.form["email"])
    if "personal_website" in request.form:
        if request.form["personal_website"] != "":
            datastax.set_website(username, request.form["personal_website"])
    if "picture_src" in request.form:
        print("Has picture src")
        if request.form["picture_src"] != "":
            print("set picture src")
            datastax.set_image(username, request.form["picture_src"])
    flash("Updated.")
    return redirect(url_for('customize'))

@app.route("/widget")
def widget():
    return render_template(
        "pages/widget.html",
        context={
            "url_username": session["username"].replace(" ", "%20"),
        }
    )

@app.route("/widget_info/<username>")
def widget_template(username):
    print('here!!!')
    conns = {
        user: {
            "full_name": user,
            "picture_src": datastax.get_image(username),
            "personal_website": datastax.get_website(username),
        }  for user in datastax.get_connections(username)
    }
    print(conns)
    t = render_template(
        "widget.js",
        context={
            'full_name': username,
            'personal_website': datastax.get_website(username),
            'picture_src': datastax.get_image(username),
            'connections': conns,
        }
    )
    print(t)
    return t

@app.route("/signup_filled", methods=["POST"])
def login_or_register():
    username = request.form.get("full_name", "")
    password = request.form.get("password", "")
    email = request.form.get("email", "")
    if "signin" in request.form:
        print("Trying to sign in!")
        if datastax.has_account(username):
            if datastax.check_credentials(username, password):
                session["username"] = username
                return redirect(url_for("customize"))
    if "register" in request.form:
        if datastax.username_free(username):
            datastax.make_account(username, password, email, "", "")
            session["username"] = username
            return redirect(url_for("customize"))
            return render_template(
                "pages/signed_up.html",
                context={"username":username}
            )
    flash("Invalid credientials.")
    return redirect(url_for('index'))

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
    print("change_connection")
    print(request.get_json())
    username = request.json.get("username", "")
    #password = request.json.get("username2", "")
    other_user = request.json.get("other_user", "")
    #if datastax.check_credentials(username, password):
    print(session)
    #username = session["username"]
    #print(username, other_username)
    datastax.change_connection(username, other_user)
    response = jsonify({"worked": True})
    response.headers.add('Access-Control-Allow-Origin', '*')
    print(response)
    print(response.headers)
    return response
    #return jsonify({"worked": False})

if __name__ == "__main__":
    app.run()
