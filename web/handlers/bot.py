from . import bot_bp


@bot_bp.route("/", methods=["GET", "POST"])
def index():
    return "Hello"
