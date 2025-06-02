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


    def to_dict(self):
        return {
            "name":self.name,
            "email":self.email,
            "id":self.id,
            "date_of_birth":self.date_of_birth,
            "password":self.password,
            "username":self.username,
            "phone_number":self.phone_number,

        }

    # organiser: Optional["Organiser"] = Relationship(back_populates="user")
    # attendee: Optional["Attendee"] = Relationship(back_populates="user")

