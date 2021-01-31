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
    email = session["email"]
    conns = {user:datastax.get_website(email) for user in datastax.get_connections(email)}
    return render_template(
        "pages/profile.html",
        context={
            'name': datastax.get_name(email),
            'personal_website': datastax.get_website(email),
            'picture_src': datastax.get_image(email),
            'connections': conns,
        }
    )

@app.route("/customize")
def customize():
    email = session["email"]
    conns = {user:datastax.get_website(email) for user in datastax.get_connections(email)}
    return render_template(
        "pages/customize.html",
        context={
            'name': datastax.get_name(email),
            'personal_website': datastax.get_website(email),
            'picture_src': datastax.get_image(email),
            'connections': conns,
            "email": email,
        }
    )

@app.route("/update_customization", methods=["POST"])
def update_customization():
    email = session["email"]
    print(request.form)
    if "name" in request.form:
        if request.form["name"] != "":
            datastax.set_name(email, request.form["name"])
    if "personal_website" in request.form:
        if request.form["personal_website"] != "":
            datastax.set_website(email, request.form["personal_website"])
    if "picture_src" in request.form:
        if request.form["picture_src"] != "":
            datastax.set_image(email, request.form["picture_src"])
    flash("Updated.")
    return redirect(url_for('customize'))

@app.route("/widget")
def widget():
    return render_template(
        "pages/widget.html",
        context={
            "email": session["email"],
        }
    )

@app.route("/widget_info/<email>")
def widget_template(email):
    print('here!!!')
    conns = {
        user_email: {
            "name": datastax.get_name(user_email),
            "picture_src": datastax.get_image(email),
            "personal_website": datastax.get_website(email),
        }  for user_email in datastax.get_connections(email)
    }
    print(conns)
    t = render_template(
        "widget.js",
        context={
            'email': email,
            'has_account': 'true' if datastax.has_account(email) else 'false',
            'name': datastax.get_name(email),
            'personal_website': datastax.get_website(email),
            'picture_src': datastax.get_image(email),
            'connections': conns,
        }
    )
    print(t)
    return t

@app.route("/signup_filled", methods=["POST"])
def login_or_register():
    email = request.form.get("email", "")
    password = request.form.get("password", "")
    name = request.form.get("name", "")
    if "signin" in request.form:
        print("Trying to sign in!")
        if datastax.has_account(email):
            if datastax.check_credentials(email, password):
                session["email"] = email
                return redirect(url_for("profile"))
    if "register" in request.form:
        if datastax.email_free(email):
            datastax.make_account(email, "", name, password, "")
            session["email"] = email
            return redirect(url_for("customize"))
            """
            return render_template(
                "pages/signed_up.html",
                context={"username":username}
            )
            """
    flash("Invalid credientials.")
    return redirect(url_for('index'))

# what is this for
@app.route("/set_website", methods=["POST"])
def set_website():
    assert "email" in session, "Email not in session!"
    website = request.form.get("website", "https://www.google.com")
    datastax.set_website(session["email"], website)

@app.route("/get_connections", methods=["POST"])
def get_connections():
    email = request.json.get("email", "")
    if not datastax.has_account(email):
        return jsonify({})
    connections = {}
    for user in datastax.get_connections(email):
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
