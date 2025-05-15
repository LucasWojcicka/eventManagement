import reflex as rx
from datetime import datetime

from eventManagement.models.attendee import Attendee
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
        events: list[Event]

        def load_all_events(self):
            with rx.session() as session:
                self.events = session.exec(Event.select()).all()

    class GetEvent():
        id: int
        event: Event

        def get_event_by_id(self):
            with rx.session() as session:
                self.event = session.exec(Event.select().where(Event.id == self.id)).first()

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

    class ChangeDuration(rx.State):
        id: int
        duration: str

        @rx.event
        def change_duration(self):
            with rx.session() as session:
                event = session.exec(
                    Event.select().where(
                        (Event.id == self.id)
                    )
                ).first()
                Event.duration = self.duration
                session.add(event)
                session.commit()

    class ChangeDate(rx.State):
        id: int
        date: datetime

        @rx.event
        def change_date(self):
            with rx.session() as session:
                event = session.exec(
                    Event.select().where(
                        (Event.id == self.id)
                    )
                ).first()
                Event.date = self.date
                session.add(event)
                session.commit()

    class ChangeLocation(rx.State):
        id: int
        location: str

        @rx.event
        def change_location(self):
            with rx.session() as session:
                event = session.exec(
                    Event.select().where(
                        (Event.id == self.id)
                    )
                ).first()
                Event.location = self.location
                session.add(event)
                session.commit()

    class ChangePriceRangeLowest(rx.State):
        id: int
        price_range_lowest: int

        @rx.event
        def change_price_range_lowest(self):
            with rx.session() as session:
                event = session.exec(
                    Event.select().where(
                        (Event.id == self.id)
                    )
                ).first()
                Event.price_range_lowest = self.price_range_lowest
                session.add(event)
                session.commit()

    class ChangePriceRangeHighest(rx.State):
        id: int
        price_range_highest: int

        @rx.event
        def change_price_range_highest(self):
            with rx.session() as session:
                event = session.exec(
                    Event.select().where(
                        (Event.id == self.id)
                    )
                ).first()
                Event.price_range_highest = self.price_range_highest
                session.add(event)
                session.commit()

    class ChangeDescription(rx.State):
        id: int
        description: str

        @rx.event
        def change_description(self):
            with rx.session() as session:
                event = session.exec(
                    Event.select().where(
                        (Event.id == self.id)
                    )
                ).first()
                Event.description = self.description
                session.add(event)
                session.commit()

    class ChangeAgeRange(rx.State):
        id: int
        age_range: str

        @rx.event
        def change_age_range(self):
            with rx.session() as session:
                event = session.exec(
                    Event.select().where(
                        (Event.id == self.id)
                    )
                ).first()
                Event.age_range = self.age_range
                session.add(event)
                session.commit()

    class ChangeAttendeesNum(rx.State):
        id: int
        attendeesNum: int

        @rx.event
        def change_attendees_num(self):
            with rx.session() as session:
                event = session.exec(
                    Event.select().where(
                        (Event.id == self.id)
                    )
                ).first()
                Event.attendees_num = self.attendeesNum
                Event.occupied_capacity = Event.occupied_capacity + self.attendeesNum
                session.add(event)
                session.commit()

    class NewAttendee(rx.State):
        id: int
        attendee: int

        @rx.event
        def new_attendee(self):
            with rx.session() as session:
                event = session.exec(
                    Event.select().where(
                        (Event.id == self.id)
                    )
                ).first()
                Event.attendees_num = self.attendee
                Event.occupied_capacity = Event.occupied_capacity + 1
                session.add(event)
                session.commit()

    class GetEmptyCapacity():
        id: int
        empty_capacity: int

        def get_remaining_capacity_count(self):
            with rx.session() as session:
                event = session.exec(
                    Event.select().where(
                        (Event.id == self.id)
                    )
                ).first()
            self.empty_capacity = event.capacity - event.occupied_capacity

    class GetAttenders():
        id: int
        attenders: list[Attendee]

        def get_attenders(self):
            with rx.session() as session:
                this_event = EventServices.GetEvent.get_event_by_id(id)
                attendees = Attendee.query.where(Attendee.events.contains(this_event)).all()
                return attendees
