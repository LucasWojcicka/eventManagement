import reflex as rx
from datetime import datetime

# from sqlmodel import col

from eventManagement.models.attendee import Attendee
from eventManagement.models.event import EventType, EventStatus, Event, Registration, Perk
# from eventManagement.models.user import User
from typing import Optional, List
from typing import Annotated

from fastapi import FastAPI, Path


class EventServices(rx.State):
    # class AddEvent(rx.State):
    #     name: str
    #     duration: int
    #     event_type: str
    #     date: datetime
    #     location: str
    #     price_range_lowest: int
    #     price_range_highest: int
    #     description: str
    #     age_range: str
    #     attendees_num: int
    #     status: str
    #     capacity: int
    #     occupied_capacity: int
    #
    #     @rx.event
    #     def add_event(self):
    #         with rx.session() as session:
    #             session.add(
    #                 Event(
    #                     name=self.name,
    #                     duration=self.duration,
    #                     event_type=self.event_type,
    #                     date=self.date,
    #                     location=self.location,
    #                     price_range_lowest=self.price_range_lowest,
    #                     price_range_highest=self.price_range_highest,
    #                     description=self.description,
    #                     age_range=self.age_range,
    #                     attendees_num=self.attendees_num,
    #                     status=self.status,
    #                     capacity=0,
    #                     occupied_capacity=self.occupied_capacity
    #                 )
    #             )
    #             session.commit()

    # getters
    @staticmethod
    def get_all_events():
        with rx.session() as session:
            return session.exec(Event.select()).all()
        # print("get all events")

    @staticmethod
    def get_event_by_id(event_id: int) -> Event | None:
        with rx.session() as session:
            return session.exec(Event.select().where(Event.id == event_id)).first()

    @staticmethod
    def get_attenders(event_id: int):
        print("get attenders of event")
        with rx.session() as session:
            all_attendees = session.exec(Attendee.select()).all()
            attenders = [
                attendee.id for attendee in all_attendees
                if any(event.id == event_id for event in attendee.events)
            ]
        return attenders

    @staticmethod
    def get_event_by_name(name: str):
        pattern = f"%{name}%"
        with rx.session() as session:
            return session.exec(Event.select().where(Event.name.like(pattern))).all()

    @staticmethod
    def get_event_by_date(date: datetime):
        with rx.session() as session:
            return session.exec(Event.select().where(Event.date == date)).all()

    # unsure VVVVVV
    @staticmethod
    def get_event_by_between_dates(start_date: datetime, end_date: datetime):
        with rx.session() as session:
            return session.exec(Event.select().where(Event.date >= start_date and Event.date <= end_date)).all()

    @staticmethod
    def get_event_by_location(location: str):
        with rx.session() as session:
            return session.exec(Event.select().where(Event.location == location)).all()

    @staticmethod
    def get_event_by_status(status: str):
        with rx.session() as session:
            return session.exec(Event.select().where(Event.status == status)).all()

    @staticmethod
    def get_event_by_type(event_type: str):
        with rx.session() as session:
            return session.exec(Event.select().where(Event.event_type == event_type)).all()

    @staticmethod
    def get_event_perks_from_event_id(event_id: int):
        with rx.session() as session:
            return session.exec(Perk.select().where(Perk.event_id == event_id)).all()

    # setters
    @staticmethod
    def set_event(name: str, duration: int, event_type: str, date: datetime,
                  location: str, price_range_lowest: int, price_range_highest: int, description: str,
                  age_range: str, status: str, capacity: int):
        new_event = Event(name=name,
                          duration=duration,
                          event_type=event_type,
                          date=date,
                          location=location,
                          price_range_lowest=price_range_lowest,
                          price_range_highest=price_range_highest,
                          description=description,
                          age_range=age_range,
                          attendees_num=0,
                          status=status,
                          capacity=capacity,
                          occupied_capacity=0
                          )
        with rx.session() as session:
            session.add(new_event)
            session.commit()
        print("make_event")

    @staticmethod
    def set_event_name(event_id: int, event_name: str):
        with rx.session() as session:
            event = EventServices.get_event_by_id(event_id)
            before = event.name
            event.name = event_name
            print(before + " -> " + event.name)
            session.add(event)
            session.commit()

    @staticmethod
    def set_event_duration(event_id: int, duration: str):
        with rx.session() as session:
            event = EventServices.get_event_by_id(event_id)
            before = event.duration
            event.duration = duration
            session.add(event)
            print(str(before) + " -> " + str(event.duration))
            session.commit()

    @staticmethod
    def set_event_event_type(event_id: int, event_type: str):
        with rx.session() as session:
            event = EventServices.get_event_by_id(event_id)
            before = event.event_type
            event.duration = event_type
            session.add(event)
            print(str(before) + " -> " + str(event.event_type))
            session.commit()

    @staticmethod
    def set_event_date(event_id: int, date: datetime):
        with rx.session() as session:
            event = EventServices.get_event_by_id(event_id)
            before = event.date
            event.date = date
            session.add(event)
            print(str(before) + " -> " + str(event.date))
            session.commit()

    @staticmethod
    def set_event_location(event_id: int, location: str):
        with rx.session() as session:
            event = EventServices.get_event_by_id(event_id)
            before = event.location
            event.location = location
            session.add(event)
            print(str(before) + " -> " + str(event.location))
            session.commit()

    @staticmethod
    def set_event_price_range_lowest(event_id: int, price_range_lowest: int):
        with rx.session() as session:
            event = EventServices.get_event_by_id(event_id)
            before = event.price_range_lowest
            event.price_range_lowest = price_range_lowest
            session.add(event)
            print(str(before) + " -> " + str(event.price_range_lowest))
            session.commit()

    @staticmethod
    def set_event_price_range_highest(event_id: int, price_range_highest: int):
        with rx.session() as session:
            event = EventServices.get_event_by_id(event_id)
            before = event.price_range_highest
            event.price_range_highest = price_range_highest
            session.add(event)
            print(str(before) + " -> " + str(event.price_range_highest))
            session.commit()

    @staticmethod
    def set_event_description(event_id: int, description: str):
        with rx.session() as session:
            event = EventServices.get_event_by_id(event_id)
            before = event.description
            event.description = description
            session.add(event)
            print(str(before) + " -> " + str(event.description))
            session.commit()

    @staticmethod
    def set_event_age_range(event_id: int, max: int, min: int):
        with rx.session() as session:
            event = EventServices.get_event_by_id(event_id)
            range = str(min) + " to " + str(max)
            before = event.age_range
            event.age_range = range
            session.add(event)
            print(str(before) + " -> " + str(event.age_range))
            session.commit()

    @staticmethod
    def set_event_event_status(event_id: int, event_status: str):
        with rx.session() as session:
            event = EventServices.get_event_by_id(event_id)
            before = event.event_status
            event.event_status = event_status
            session.add(event)
            print(str(before) + " -> " + str(event.event_status))
            session.commit()

    @staticmethod
    def set_event_capacity(event_id: int, capacity: int):
        with rx.session() as session:
            event = EventServices.get_event_by_id(event_id)
            before = event.capacity
            event.capacity = capacity
            session.add(event)
            print(str(before) + " -> " + str(event.capacity))
            session.commit()

# @staticmethod
# def get_organised_events(organiser_id: int):
#     print("get organiser events")

# class GetEventByIDWithRXState(rx.State):
#     event_id: int
#
# @rx.event
# def get_event_by_id_reflex_event(self, event_id: int):
#     with rx.session() as session:
#         self.event_id = event_id
#         return session.exec(Event.select().where(Event.id == event_id)).first()

# works V


# class GetEvent():
#     given_id: int
#     event_found: Event
#
#     # @rx.event
#     def get_event_by_id(self):
#         with rx.session() as session:
#             # self.given_id = 1
#             event = session.exec(
#                 Event.select().where(Event.id == self.given_id)
#             ).first()
#             self.event_found = event


# class ChangeName(rx.State):
#     id: int
#     name: str
#
#     @rx.event
#     def change_name(self):
#         with rx.session() as session:
#             event = session.exec(
#                 Event.select().where(
#                     (Event.id == self.id)
#                 )
#             ).first()
#             Event.username = self.username
#             session.add(event)
#             session.commit()
#
#
# class ChangeDuration(rx.State):
#     id: int
#     duration: str
#
#     @rx.event
#     def change_duration(self):
#         with rx.session() as session:
#             event = session.exec(
#                 Event.select().where(
#                     (Event.id == self.id)
#                 )
#             ).first()
#             Event.duration = self.duration
#             session.add(event)
#             session.commit()
#
#
# class ChangeDate(rx.State):
#     id: int
#     date: datetime
#
#     @rx.event
#     def change_date(self):
#         with rx.session() as session:
#             event = session.exec(
#                 Event.select().where(
#                     (Event.id == self.id)
#                 )
#             ).first()
#             Event.date = self.date
#             session.add(event)
#             session.commit()
#
#
# class ChangeLocation(rx.State):
#     id: int
#     location: str
#
#     @rx.event
#     def change_location(self):
#         with rx.session() as session:
#             event = session.exec(
#                 Event.select().where(
#                     (Event.id == self.id)
#                 )
#             ).first()
#             Event.location = self.location
#             session.add(event)
#             session.commit()
#
#
# class ChangePriceRangeLowest(rx.State):
#     id: int
#     price_range_lowest: int
#
#     @rx.event
#     def change_price_range_lowest(self):
#         with rx.session() as session:
#             event = session.exec(
#                 Event.select().where(
#                     (Event.id == self.id)
#                 )
#             ).first()
#             Event.price_range_lowest = self.price_range_lowest
#             session.add(event)
#             session.commit()
#
#
# class ChangePriceRangeHighest(rx.State):
#     id: int
#     price_range_highest: int
#
#     @rx.event
#     def change_price_range_highest(self):
#         with rx.session() as session:
#             event = session.exec(
#                 Event.select().where(
#                     (Event.id == self.id)
#                 )
#             ).first()
#             Event.price_range_highest = self.price_range_highest
#             session.add(event)
#             session.commit()
#
#
# class ChangeDescription(rx.State):
#     id: int
#     description: str
#
#     @rx.event
#     def change_description(self):
#         with rx.session() as session:
#             event = session.exec(
#                 Event.select().where(
#                     (Event.id == self.id)
#                 )
#             ).first()
#             Event.description = self.description
#             session.add(event)
#             session.commit()
#
#
# class ChangeAgeRange(rx.State):
#     id: int
#     age_range: str
#
#     @rx.event
#     def change_age_range(self):
#         with rx.session() as session:
#             event = session.exec(
#                 Event.select().where(
#                     (Event.id == self.id)
#                 )
#             ).first()
#             Event.age_range = self.age_range
#             session.add(event)
#             session.commit()
#
#
# class ChangeAttendeesNum(rx.State):
#     id: int
#     attendeesNum: int
#
#     @rx.event
#     def change_attendees_num(self):
#         with rx.session() as session:
#             event = session.exec(
#                 Event.select().where(
#                     (Event.id == self.id)
#                 )
#             ).first()
#             Event.attendees_num = self.attendeesNum
#             Event.occupied_capacity = Event.occupied_capacity + self.attendeesNum
#             session.add(event)
#             session.commit()
#
#
# class NewAttendee(rx.State):
#     id: int
#     attendee: int
#
#     @rx.event
#     def new_attendee(self):
#         with rx.session() as session:
#             event = session.exec(
#                 Event.select().where(
#                     (Event.id == self.id)
#                 )
#             ).first()
#             Event.attendees_num = self.attendee
#             Event.occupied_capacity = Event.occupied_capacity + 1
#             session.add(event)
#             session.commit()
#
#
# class GetEmptyCapacity():
#     id: int
#     empty_capacity: int
#
#     def get_remaining_capacity_count(self):
#         with rx.session() as session:
#             event = session.exec(
#                 Event.select().where(
#                     (Event.id == self.id)
#                 )
#             ).first()
#         self.empty_capacity = event.capacity - event.occupied_capacity
#
#
# class GetAttenders():
#     id: int
#     attenders: list[Attendee]
#
#     def get_attenders(self):
#         with rx.session() as session:
#             this_event = EventServices.GetEvent.get_event_by_id(id)
#             attendees = Attendee.query.where(Attendee.events.contains(this_event)).all()
#             return attendees
#
#
# class GetEventRegistrations():
#     id: int
#     registrations: list[Registration]
#
#     def get_registrations(self):
#         with rx.session() as session:
#             registrations = Registration.query.where(Registration.event_id == self.id).all()
#             return registrations
#
#
# class GetApprovedEventRegistrations():
#     id: int
#     approved_registrations: list[Registration]
#
#     def get_approved_registrations(self):
#         with rx.session() as session:
#             registrations = EventServices.GetEventRegistrations.get_registrations(id)
#             approved_registrations = registrations.query.where(Registration.approved == True).all()
#             return approved_registrations
#
#
# class GetDisapprovedEventRegistrations():
#     id: int
#     approved_registrations: list[Registration]
#
#     def get_disapproved_registrations(self):
#         with rx.session() as session:
#             registrations = EventServices.GetEventRegistrations.get_registrations(id)
#             approved_registrations = registrations.query.where(Registration.approved != True).all()
#             return approved_registrations
