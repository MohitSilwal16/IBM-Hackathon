from flask import Flask
from db import db
from handlers.auth import auth_bp
from handlers.bot import bot_bp
from handlers.ticket import UPLOAD_FOLDER, ticket_bp

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///complaint.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.register_blueprint(auth_bp)
app.register_blueprint(bot_bp)
app.register_blueprint(ticket_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
