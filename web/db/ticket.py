from . import db
from sqlalchemy import or_, CheckConstraint
from datetime import datetime

class Ticket(db.Model):
    __tablename__ = "tickets"

    ticket_id = db.Column(db.String(20), primary_key=True)
    user_email = db.Column(db.String(30), db.ForeignKey("users.email"), nullable=False)
    question1 = db.Column(db.String(100), nullable=False)
    question2 = db.Column(db.String(100), nullable=False)
    question3 = db.Column(db.String(100), nullable=False)
    question4 = db.Column(db.String(100), nullable=False)
    question5 = db.Column(db.String(100), nullable=False)
    question6 = db.Column(db.String(100), nullable=False)
    question7 = db.Column(db.String(100), nullable=False)
    question8 = db.Column(db.String(100), nullable=False)
    other_description = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    remark = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    priority = db.Column(db.String(10), nullable=False)

    __table_args__ = (
        CheckConstraint("status IN ('Registered', 'In Progress', 'Resolved')", name='check_status_valid'),
        CheckConstraint("priority IN ('Urgent', 'High', 'Medium', 'Low')", name='check_priority_valid'),
        CheckConstraint("question1 IN ('A', 'B', 'C', 'D', 'E', 'F', 'G')", name='check_question1_validity'),
        CheckConstraint("question2 IN ('A', 'B', 'C', 'D')", name='check_question2_validity'),
        CheckConstraint("question3 IN ('A', 'B', 'C', 'D')", name='check_question3_validity'),
        CheckConstraint("question4 IN ('A', 'B', 'C', 'D')", name='check_question4_validity'),
        CheckConstraint("question5 IN ('A', 'B', 'C')", name='check_question5_validity'),
        CheckConstraint("question6 IN ('A', 'B', 'C')", name='check_question6_validity'),
        CheckConstraint("question7 IN ('A', 'B', 'C', 'D')", name='check_question7_validity'),
        CheckConstraint("question8 IN ('A', 'B', 'C')", name='check_question8_validity'),
    )

def add_complaint(ticket: Ticket) -> None:
    db.session.add(ticket)
    db.session.commit()

def get_Ticket_by_username(username: str) -> list[Ticket]:
    return (
        Ticket.query.filter(
            Ticket.user_email == username
        )
        .all()
    )
