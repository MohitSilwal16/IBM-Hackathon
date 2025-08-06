from . import bot_bp
from handlers.ticket import UPLOAD_FOLDER
from chatbot import chatbot
from flask import request, render_template, redirect, url_for
from db import users, ticket
from utils import tokens
from chatbot.chatbot import get_severity_level, get_category

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bot_bp.route("/", methods=["GET"])
def home():
    session_token = request.cookies.get("session-token")
    is_session_token_valid = users.is_session_token_valid(session_token)
    if not is_session_token_valid:
        return redirect(url_for("auth.login"))

    email = users.get_email_by_token(session_token)
    t = ticket.get_ticket_by_email(email)
    t = t[:3]

    return render_template("home.html", user_complain="", bot_response="", tickets=t)


@bot_bp.route("/message", methods=["POST"])
def message():
    session_token = request.cookies.get("session-token")
    is_session_token_valid = users.is_session_token_valid(session_token)
    if not is_session_token_valid:
        return redirect(url_for("auth.about"))

    email = users.get_email_by_token(session_token)
    ticks = ticket.get_ticket_by_email(email)
    ticks = ticks[:3]

    user_complain = request.form.get("com")
    # TODO: TEMP START
    # if user_complain == "Hello":
    #     return render_template(
    #         "home.html",
    #         user_complain=user_complain,
    #         bot_response="How're you ?",
    #         tickets=ticks,
    #     )
    # TODO: TEMP END

    bot_res = request.form.get("bot_response")
    print(f"Bot Response: {bot_res}")
    if not bot_res:
        bot_res = chatbot.get_complain_solution(user_complain)
        print(f"User Complain: {user_complain}")
        return render_template(
            "home.html",
            user_complain=user_complain,
            bot_response=bot_res,
            tickets=ticks,
        )

    # Create Ticket
    main_desc = request.form.get("main_desc")
    print(f"Main Desc: {main_desc}")
    complain_image = request.files.get("image")
    print(f"Image: {complain_image}")
    print(f"Image: {complain_image.filename}")
    image_url = ""
    ticket_id = "TCK-" + tokens.generate_random_tokens(4)

    # if complain_image and allowed_file(complain_image.filename):
    if complain_image:
        print("Got Valid Image")
        filepath = UPLOAD_FOLDER + "\\" + ticket_id + ".jpg"
        complain_image.save(filepath)
        image_url = filepath.replace("\\", "/")  # Make it Browser-friendly

    priority = get_severity_level(user_complain=user_complain)
    category = get_category(user_complain=user_complain)

    print(f"Priority: {priority}")
    print(f"Category: {category}")

    t = ticket.Ticket(
        ticket_id=ticket_id,
        user_email=email,
        main_description=main_desc,
        other_description=user_complain,
        status="Registered",
        remark="",
        category=category,
        priority=priority,
        image_url=image_url,
    )
    ticket.add_ticket(t)

    ticks = ticket.get_ticket_by_email(email)
    ticks = ticks[:3]
    return render_template(
        "home.html", user_complain="", bot_response="", tickets=ticks
    )
