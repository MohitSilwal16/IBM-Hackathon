from . import ticket_bp
from flask import request, make_response, render_template, redirect, url_for
from db import users, ticket
from ticket import get_tickets

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

@ticket_bp.route("/ticket", methods=["GET"])
def get_tickets():
    session_token = request.cookies.get("session-token")
    is_session_token_valid = users.is_session_token_valid(session_token)
    if not is_session_token_valid:
        return redirect(url_for("auth.about"))
    
    email = users.get_email_by_token(session_token)
    t = ticket.get_ticket_by_email(email)

    return render_template("tickets.html")