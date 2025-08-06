from . import bot_bp
from chatbot import chatbot
from flask import request, make_response, render_template, redirect, url_for
from db import users

@bot_bp.route("/", methods=["GET"])
def home():
    session_token = request.cookies.get("session-token")
    is_session_token_valid = users.is_session_token_valid(session_token)
    if not is_session_token_valid:
        return redirect(url_for("auth.login"))
    return render_template("home.html")

@bot_bp.route("/message", methods = ['POST'])
def message():
    session_token = request.cookies.get("session-token")
    is_session_token_valid = users.is_session_token_valid(session_token)
    if not is_session_token_valid:
        return redirect(url_for("auth.about"))

    user_complain = request.get("com")
    chatbot_res = chatbot.get_complain_solution(user_complain)
    print(f"Chat Bot Response: {chatbot_res}")
    return render_template("home.html")