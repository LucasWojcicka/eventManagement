import reflex as rx
from sqlmodel import Field, Relationship, SQLModel

"""
Linking table between Attendee's and Events
"""

class AttendeeEventLink(rx.Model, table=True):
    attendee_id: int = Field(foreign_key="attendee.id", primary_key=True)
    event_id: int = Field(foreign_key="event.id", primary_key=True)
