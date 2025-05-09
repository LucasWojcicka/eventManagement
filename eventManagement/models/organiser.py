import datetime
from typing import List, Optional

import reflex as rx
from sqlmodel import Field
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

from eventManagement.models.event import Event
from eventManagement.models.user import User


class Organiser(rx.Model, table=True):
    user: "User" = Relationship(
    )

    organised_events: Optional[list["Event"]] = Relationship(
    )