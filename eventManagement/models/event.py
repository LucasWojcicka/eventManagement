import reflex as rx
from typing import List, Optional
from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, Integer, Column
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

# from eventManagement.models.organiser import Organiser
# from eventManagement.models.attendee import Attendee

from sqlmodel import Field, Relationship
from typing import Optional, List

# from eventManagement.models.event_links import EventTiers, EventRegistrations
# from eventManagement.models.event_links import EventTiers


# from eventManagement.models.attendee import Attendee


class EventType(Enum):
    CONCERT = "concert"
    CONFERENCE = "conference"
    NETWORKING = "networking"
    EXHIBITION = "exhibition"

    @staticmethod
    def list():
        return list(map(lambda t: t, EventType))


class EventStatus(Enum):
    NORMAL = "normal"
    CANCELLED = "cancelled"
    POSTPONED = "postponed"

    @staticmethod
    def list():
        return list(map(lambda t: t, EventStatus))


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


class Registration(rx.Model, table=True):
    id: int = Field(primary_key=True)
    registration_type: str
    registration_type_perks: Optional[str]
    description: str
    price: int
    approved: bool
    # approved: bool | None
    event_id: int = Field(
        default=None,
        foreign_key="event.id"
    )

    event: "Event" = Relationship(
    )


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
    # perks: list[Perk] = Relationship(link_model=EventTiers)
    # registrations: list[Registration] = Relationship(link_model=EventRegistrations)

    # attendees: List["Attendee"] = Relationship(
    #     back_populates="events",
    #     link_model=AttendeeEventLink
    # )


# import datetime
# from typing import List, Optional, TYPE_CHECKING
#
# import reflex as rx
# from sqlmodel import Field, Relationship, SQLModel

from eventManagement.models.attendee_event_link import AttendeeEventLink

# if TYPE_CHECKING:
#     from eventManagement.models.attendee import Attendee


# class Event(rx.Model, table=True):
#     id: int = Field(primary_key=True)
#     name: str
#     duration: int
#     event_type: str  # or your custom Enum
#     date: datetime.datetime
#     location: str
#     price_range_lowest: int
#     price_range_highest: int
#     description: str
#     age_range: str
#     attendees_num: int = 0
#     status: str  # or your custom Enum
#     capacity: int
#     occupied_capacity: int

# attendees: List[Attendee] = Relationship(
#     back_populates="events",
#     link_model=AttendeeEventLink
# )


# class Perks(rx.Model, table=True):
#     name: str
#     price: int
#     description: str
#     age_range: str
#     duration: int
#     available_slots: int
#
#
# class Registration(rx.Model, table=True):
#     registration_type: str
#     registration_type_perks: Optional[str]
#     # registration_type_perks: Optional[list["Perks"]]
#     description: str
#     price: int
#     approved: bool
#
#
# class Event(rx.Model, table=True):
#     name: str
#     duration: int
#     event_type: EventType
#     date: datetime
#     location: str
#     price_range_lowest: int
#     price_range_highest: int
#     description: str
#     age_range: str
#     event_id: int
#     attendees_num: int = 0
#     # registration_types: list[Registration]
#     # available_perks: list[Perks]
#     status: EventStatus
#     capacity: int
#     occupied_capacity: int
#
#     # organiser: Optional["Organiser"] = Relationship(back_populates="organised_events")
#     # attendees: Optional[list["Attendee"]] = Relationship(back_populates="attending_events")
