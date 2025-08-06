from . import bot_bp
from flask import request, make_response, render_template, redirect, url_for
from db import users

@bot_bp.route("/", methods = ['GET'])
def home():
    session_token = request.cookies.get("session-token")
    is_session_token_valid = users.is_session_token_valid(session_token)
    if not is_session_token_valid:
        return redirect(url_for("auth.about"))

    return render_template("home.html")