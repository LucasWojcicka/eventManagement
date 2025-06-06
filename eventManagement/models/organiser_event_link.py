
import reflex as rx
from sqlmodel import Field, Relationship, SQLModel


"""
Linking table between Organisers and Events
"""
class OrganiserEventLink(rx.Model, table=True):
    organiser_id: int = Field(foreign_key="organiser.id", primary_key=True)
    event_id: int = Field(foreign_key="event.id", primary_key=True)

