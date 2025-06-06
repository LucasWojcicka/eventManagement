import reflex as rx
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine
from eventManagement.models.organiser_event_link import OrganiserEventLink

from eventManagement.models.event import Event
from eventManagement.models.user import User

"""
data model for Organiser. Each organiser has a one to one relationship with User.
Organised Events are accessible to organiser via OrganiserEventLink
"""

class Organiser(rx.Model, table=True):
    user_id: int = Field(default=None, foreign_key="user.id")
    events: list[Event] = Relationship(link_model=OrganiserEventLink)
    user: "User" = Relationship(
    )

