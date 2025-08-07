from . import db
from sqlalchemy import or_, CheckConstraint, case


class Ticket(db.Model):
    __tablename__ = "tickets"

    ticket_id = db.Column(db.String(20), primary_key=True)
    user_email = db.Column(db.String(30), db.ForeignKey("users.email"), nullable=False)
    main_description = db.Column(db.String(500), nullable=False)
    other_description = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    remark = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    priority = db.Column(db.String(10), nullable=False)
    image_url = db.Column(db.String(100))

    __table_args__ = (
        CheckConstraint(
            "status IN ('Registered', 'In Progress', 'Resolved')",
            name="check_status_valid",
        ),
        CheckConstraint(
            "priority IN ('Urgent', 'High', 'Medium', 'Low')",
            name="check_priority_valid",
        ),
    )


def add_ticket(ticket: Ticket) -> None:
    db.session.add(ticket)
    db.session.commit()


def get_ticket_by_email(email: str) -> list[Ticket]:
    return Ticket.query.filter(Ticket.user_email == email).all()


def get_resolved_tickets() -> list[Ticket]:
    return Ticket.query.filter(Ticket.status == "Resolved").all()


def get_all_tickets_sorted_by_priority() -> list[Ticket]:
    priority_order = case(
        (Ticket.priority == "Urgent", 4),
        (Ticket.priority == "High", 3),
        (Ticket.priority == "Medium", 2),
        (Ticket.priority == "Low", 1),
        else_=0,
    )
    return Ticket.query.order_by(priority_order).all()


def get_all_tickets_by_email_sorted_by_priority(email: str) -> list[Ticket]:
    priority_order = case(
        (Ticket.priority == "Urgent", 4),
        (Ticket.priority == "High", 3),
        (Ticket.priority == "Medium", 2),
        (Ticket.priority == "Low", 1),
        else_=0,
    )
    return (
        Ticket.query.filter(Ticket.user_email == email).order_by(priority_order).all()
    )


def get_ticket_by_ticket_id(ticket_id: str) -> Ticket:
    return Ticket.query.filter_by(ticket_id=ticket_id).first()


def update_remarks(ticket_id: str, remarks: str) -> None:
    t = Ticket.query.filter(ticket_id=ticket_id).first()
    if not t:
        return None
    t.remarks = remarks
    db.session.commit()
