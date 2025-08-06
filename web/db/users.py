from . import db


class User(db.Model):
    __tablename__ = "users"

    email = db.Column(db.String(30), primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    session_token = db.Column(db.String(4), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


def create_user(user: User) -> None:
    db.session.add(user)
    db.session.commit()


def verify_password(email: str, password: str) -> bool:
    return User.query.filter_by(email=email, password=password).first() != None


def update_session_token(email: str, password: str, session_token: str) -> None:
    user = User.query.filter_by(email=email, password=password).first()
    if not user:
        return

    user.session_token = session_token
    db.session.commit()


def is_session_token_valid(session_token: str) -> bool:
    if session_token == "":
        return False
    return User.query.filter_by(session_token=session_token).first() != None


def revoke_session_token(session_token: str) -> None:
    user = User.query.filter_by(session_token=session_token).first()
    if not user:
        return
    user.session_token = ""
    db.session.commit()


def is_email_already_taken(email: str) -> bool:
    return User.query.filter_by(email=email).first() != None


def get_email_by_token(session_token: str) -> str:
    return User.query.filter_by(session_token=session_token).first().email
