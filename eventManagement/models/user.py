import datetime
from typing import Optional

import reflex as rx
from sqlmodel import Field
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

# from eventManagement.models import Attendee


# from eventManagement.models.organiser import Organiser
# from eventManagement.models.attendee import Attendee

class User(rx.Model, table=True):
    name: str
    email: str
    id: int = Field(primary_key=True)
    date_of_birth: datetime.date
    password: str
    username: str
    phone_number: str


    # organiser: Optional["Organiser"] = Relationship(back_populates="user")
    # attendee: Optional["Attendee"] = Relationship(back_populates="user")

