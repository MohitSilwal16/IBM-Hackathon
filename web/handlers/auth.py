from . import auth_bp
from flask import request, make_response, render_template, redirect, url_for
from utils.tokens import generate_session_tokens
from db import users, ticket

SESSION_TOKEN_LENGTH = 4

@auth_bp.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@auth_bp.route("/profile", methods=["GET"])
def profile():
    session_token = request.cookies.get("session-token")
    is_session_token_valid = users.is_session_token_valid(session_token)
    if not is_session_token_valid:
        return redirect(url_for("auth.about"))
    
    email = users.get_email_by_token(session_token)
    ticks = ticket.get_ticket_by_email(email)
    t_len = len(ticks)
    username = users.get_username_from_token(session_token)
    return render_template("profile.html", email=email, username=username, t_len=t_len)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    is_email_already_taken = users.is_email_already_taken(email)
    print(f"Is email already taken: {is_email_already_taken}")
    if is_email_already_taken:
        return render_template("register.html", error_msg="Username Already Exists")
    session_token = generate_session_tokens(SESSION_TOKEN_LENGTH)

    user_obj = users.User(
        email=email,
        username=username,
        password=password,
        session_token=session_token,
    )
    users.create_user(user_obj)

    res = make_response(redirect(url_for("bot.home")))
    res.set_cookie("session-token", session_token)
    return res


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    user_authenticated = users.verify_password(email, password)
    if not user_authenticated:
        return render_template("login.html", error_msg="Invalid Credentials")

    session_token = generate_session_tokens(SESSION_TOKEN_LENGTH)
    users.update_session_token(email, password, session_token)

    res = make_response(redirect(url_for("bot.home")))
    res.set_cookie("session-token", session_token)
    return res


@auth_bp.route("/logout", methods=["GET"])
def logout():
    session_token = request.cookies.get("session-token")
    users.revoke_session_token(session_token)

    res = make_response(redirect(url_for("auth.login")))
    res.set_cookie("session-token", "")
    return res
