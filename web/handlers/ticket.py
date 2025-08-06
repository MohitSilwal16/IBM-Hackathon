from . import ticket_bp
from flask import request, make_response, render_template, redirect, url_for
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

@ticket_bp.route("/ticket", methods=["GET"])
def ticket():
    return render_template("ticket.html")