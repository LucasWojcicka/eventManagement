import reflex as rx
import datetime

from eventManagement.models.event import EventType, EventStatus, Event
# from eventManagement.models.user import User
from typing import Optional, List


class EventServices(rx.State):
    class AddEvent(rx.State):
        name: str
        duration: int
        event_type: EventType
        date: datetime
        location: str
        price_range_lowest: int
        price_range_highest: int
        description: str
        age_range: str
        attendees_num: int
        status: EventStatus
        capacity: int
        occupied_capacity: int

        @rx.event
        def add_event(self):
            with rx.session() as session:
                session.add(
                    Event(
                        name=self.name,
                        duration=self.duration,
                        event_type=self.event_type,
                        date=self.date,
                        location=self.location,
                        price_range_lowest=self.price_range_lowest,
                        price_range_highest=self.price_range_highest,
                        description=self.description,
                        age_range=self.age_range,
                        attendees_num=self.attendees_num,
                        status=self.status,
                        capacity=0,
                        occupied_capacity=self.occupied_capacity
                    )
                )
                session.commit()

    # works V
    class LoadEvents():
        users: list[Event]

        def load_all_users(self):
            with rx.session() as session:
                self.users = session.exec(Event.select()).all()

    class ChangeName(rx.State):
        id: int
        name: str

        @rx.event
        def change_name(self):
            with rx.session() as session:
                event = session.exec(
                    Event.select().where(
                        (Event.id == self.id)
                    )
                ).first()
                Event.username = self.username
                session.add(event)
                session.commit()
