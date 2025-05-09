import reflex as rx
from typing import List, Optional
from datetime import datetime
from enum import Enum
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

# from eventManagement.models.organiser import Organiser
# from eventManagement.models.attendee import Attendee


class EventType(Enum):
    CONCERT = "concert"
    CONFERENCE = "conference"
    NETWORKING = "networking"
    EXHIBITION = "exhibition"


class EventStatus(Enum):
    NORMAL = "normal"
    CANCELLED = "cancelled"
    POSTPONED = "postponed"


class Perks(rx.Model, table=True):
    name: str
    price: int
    description: str
    age_range: str
    duration: int
    available_slots: int


class Registration(rx.Model, table=True):
    registration_type: str
    registration_type_perks: Optional[str]
    # registration_type_perks: Optional[list["Perks"]]
    description: str
    price: int
    approved: bool


class Event(rx.Model, table=True):
    name: str
    duration: int
    event_type: EventType
    date: datetime
    location: str
    price_range_lowest: int
    price_range_highest: int
    description: str
    age_range: str
    event_id: int
    attendees_num: int = 0
    # registration_types: list[Registration]
    # available_perks: list[Perks]
    status: EventStatus
    capacity: int
    occupied_capacity: int
    
    # organiser: Optional["Organiser"] = Relationship(back_populates="organised_events")
    # attendees: Optional[list["Attendee"]] = Relationship(back_populates="attending_events")
