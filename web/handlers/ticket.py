from . import ticket_bp
from flask import request, make_response, render_template, redirect, url_for
from db import users, ticket

UPLOAD_FOLDER = "static/"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

@ticket_bp.route("/ticket", methods=["GET"])
def get_tickets():
    session_token = request.cookies.get("session-token")
    is_session_token_valid = users.is_session_token_valid(session_token)
    if not is_session_token_valid:
        return redirect(url_for("auth.about"))
    
    email = users.get_email_by_token(session_token)
    print(f"Email: {email}")
    if email == "admin@gmail.com":
        ticks = ticket.get_all_tickets()
    else:
       ticks = ticket.get_ticket_by_email(email)
    t_len = len(ticks)
    t_resolved = 0
    t_inprogress = 0
    t_registered = 0
    for tick in ticks:
        if tick.status == "In Progress":
            t_inprogress+=1
        elif tick.status == "Resolved":
            t_resolved+=1
        else:
            t_registered+=1
    return render_template("tickets.html", tickets=ticks, length=t_len, t_inprogress=t_inprogress, t_resolved=t_resolved, t_registered=t_registered)

@ticket_bp.route("/ticket_details", methods=['GET'])
def ticket_details():
    return render_template("ticket_details.html")
