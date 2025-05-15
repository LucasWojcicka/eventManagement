import datetime
from typing import List, Optional

import reflex as rx
from sqlmodel import Field
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

from eventManagement.models.event import Event
from eventManagement.models.user import User


class Organiser(rx.Model, table=True):
    # user_id : int = Field(default=None, foreign_key="user.id")
    user_id : int = Field(default=None, foreign_key="user.id")

    user: "User" = Relationship(
    )

    # user: "User" = Relationship(
    #     back_populates="organiser"
    # )
    #
    # organised_events: Optional[list["Event"]] = Relationship(
    #     back_populates="organiser"
    # )
