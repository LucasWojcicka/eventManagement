

import reflex as rx
from sqlmodel import Field, Relationship

from eventManagement.models.event import Event


class Attendee(rx.Model, table=True):
    user_id: int = Field(default=None, foreign_key="user.id")
    # events: list[Event] = rx.Model.list_field(Event, link_model=True)

    user: "User" = Relationship()

