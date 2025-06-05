import reflex as rx
from datetime import datetime
from enum import Enum

from sqlmodel import Field, Relationship
from typing import Optional, List


"""
Enumeration for possible Event Types
"""
class EventType(Enum):
    CONCERT = "concert"
    CONFERENCE = "conference"
    NETWORKING = "networking"
    EXHIBITION = "exhibition"

    @staticmethod
    def list():
        return list(map(lambda t: t, EventType))

    @staticmethod
    def to_dict():
        return {e.value: e.value.capitalize() for e in EventType}

"""
Enumeration for possible Event Statuses
"""
class EventStatus(Enum):
    NORMAL = "normal"
    CANCELLED = "cancelled"
    POSTPONED = "postponed"

    @staticmethod
    def list():
        return list(map(lambda t: t, EventStatus))

    @staticmethod
    def to_dict():
        return {e.value: e.value.capitalize() for e in EventType}

"""
Data Model for Event Perk. Each perk has a relationship to Event
"""
class Perk(rx.Model, table=True):
    id: int = Field(primary_key=True)
    name: str
    price: int
    description: str
    age_range: str
    duration: int
    available_slots: int
    event_id: int = Field(
        default=None,
        foreign_key="event.id"
    )
    event: "Event" = Relationship(
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price" : self.price,
            "description" : self.description,
            "age_range" : self.age_range,
            "duration" : self.duration,
            "available_slots" : self.available_slots,
            "event_id" : self.event_id
        }


"""
Data Model for Event Registration. Each registration has a relationship to Event
"""
class Registration(rx.Model, table=True):
    id: int = Field(primary_key=True)
    perk_id : int
    price: int
    registration_date : datetime
    approved_date : Optional[datetime]
    approved: bool
    user_id : int
    # approved: bool | None
    event_id: int = Field(
        default=None,
        foreign_key="event.id"
    )

    event: "Event" = Relationship(
    )

    def to_dict(self):
        return {
            "id": self.id,
            "perk_id" : self.perk_id,
            "price" : self.price,
            "registration_date" : self.registration_date,
            "approved_date" : self.approved_date,
            "approved" : self.approved,
            "user_id" : self.user_id,
            "event_id" : self.event_id
        }


"""
Data Model for Event
"""
class Event(rx.Model, table=True):
    id: int = Field(primary_key=True)
    name: str
    duration: int
    # event_type: EventType
    event_type: str
    date: datetime
    location: str
    price_range_lowest: int
    price_range_highest: int
    description: str
    age_range: str
    attendees_num: int = 0
    # status: EventStatus
    status: str
    capacity: int
    occupied_capacity: int

    def to_dict(self):
        return {
            "event_type": self.event_type,
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "price_range_highest": self.price_range_highest,
            "age_range": self.age_range,
            "status": self.status,
            "occupied_capacity": self.occupied_capacity,
            "date": self.date.isoformat() if self.date else None,
            "duration": self.duration,
            "price_range_lowest": self.price_range_lowest,
            "description": self.description,
            "attendees_num": self.attendees_num,
            "capacity": self.capacity,

        }

