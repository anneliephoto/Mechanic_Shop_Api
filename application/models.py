from sqlalchemy.orm import Mapped, mapped_column

from application.extensions import Base, db


service_mechanics = db.Table(
    "service_mechanics",
    Base.metadata,
    db.Column("service_ticket_id", db.ForeignKey("service_tickets.id")),
    db.Column("mechanic_id", db.ForeignKey("mechanics.id")),
)


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    service_tickets: Mapped[list["ServiceTicket"]] = db.relationship(back_populates="customer")


class ServiceTicket(Base):
    __tablename__ = "service_tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(255), nullable=False)
    service_date: Mapped[str] = mapped_column(db.String(255), nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(255), nullable=False)

    customer_id: Mapped[int] = mapped_column(db.ForeignKey("customers.id"))
    customer: Mapped["Customer"] = db.relationship(back_populates="service_tickets")
    mechanics: Mapped[list["Mechanic"]] = db.relationship(
        secondary=service_mechanics,
        back_populates="service_tickets",
    )


class Mechanic(Base):
    __tablename__ = "mechanics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)
    service_tickets: Mapped[list["ServiceTicket"]] = db.relationship(
        secondary=service_mechanics,
        back_populates="mechanics",
    )
