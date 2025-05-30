from sqlmodel import SQLModel
import datetime
from typing import List, Optional, TYPE_CHECKING

import reflex as rx
from sqlmodel import Field, Relationship, SQLModel


class AttendeeEventLink(rx.Model, table=True):
    attendee_id: int = Field(foreign_key="attendee.id", primary_key=True)
    event_id: int = Field(foreign_key="event.id", primary_key=True)
