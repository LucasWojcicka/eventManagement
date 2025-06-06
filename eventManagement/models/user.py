import datetime
import reflex as rx
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine


"""
data model for User Table
"""

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
            "name": self.name,
            "email": self.email,
            "id": self.id,
            "date_of_birth": self.date_of_birth,
            "password": self.password,
            "username": self.username,
            "phone_number": self.phone_number,

        }

