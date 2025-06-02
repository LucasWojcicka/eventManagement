from sqlmodel import SQLModel
import datetime
from typing import List, Optional, TYPE_CHECKING

import reflex as rx
from sqlmodel import Field, Relationship, SQLModel


class OrganiserEventLink(rx.Model, table=True):
    organiser_id: int = Field(foreign_key="organiser.id", primary_key=True)
    event_id: int = Field(foreign_key="event.id", primary_key=True)

