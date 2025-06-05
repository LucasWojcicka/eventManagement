import reflex as rx
from sqlmodel import Field, Relationship

from eventManagement.models.attendee_event_link import AttendeeEventLink
from eventManagement.models.event import Event

"""
data model for Attendee. Each attendee has a one to one relationship with User.
Attending Events are accessible to attendee via AttendeeEventLink
"""
class Attendee(rx.Model, table=True):
    user_id: int = Field(default=None, foreign_key="user.id")
    events: list[Event] = Relationship(link_model=AttendeeEventLink)
    user: "User" = Relationship()

    def to_dict(self):
        return {
            "user_id": self.user_id

        }
