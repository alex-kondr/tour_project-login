from typing import Optional, List

from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin

from data.base import Base


class Tour(Base):
    __tablename__ = "tours"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(100))
    departure: Mapped[str] = mapped_column(String(100))
    picture: Mapped[str] = mapped_column(String(500))
    price: Mapped[int] = mapped_column()
    stars: Mapped[str] = mapped_column(String(5))
    country: Mapped[str] = mapped_column(String(100))
    nights: Mapped[int] = mapped_column()
    date: Mapped[str] = mapped_column(String(100))


tour_user_assoc = Table(
    "tour_user_assoc",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("tour_id", ForeignKey("tours.id"), primary_key=True)
)


class User(Base, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(500))
    password: Mapped[str] = mapped_column(String(500))
    tours: Mapped[List[Tour]] = relationship(secondary=tour_user_assoc)
