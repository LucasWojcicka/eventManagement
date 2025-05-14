import datetime
import random
import time

import reflex as rx
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlmodel import Session
from faker import Faker

from eventManagement.models.user import User
from eventManagement.models.event import Event, EventType, EventStatus
from eventManagement.models.attendee import Attendee
from eventManagement.models.organiser import Organiser


def seed_users():
    fake = Faker()
    print("seed users")
    with rx.session() as session:
        # existing_data = session.exec(User.select()).first()
        # if existing_data:
        #     print(f"already data, pass: {existing_data}")
        #     # session.exec(sqlalchemy.text("DELETE FROM User"))
        #     # session.exec(sqlalchemy.text("VACUUM"))
        #     # session.commit()
        #     # return
        # else:
        engine = create_engine("sqlite:///reflex.db")

        session.exec(sqlalchemy.text("DELETE FROM User"))
        # session.exec(sqlalchemy.text("VACUUM"))
        session.commit()
        for x in range(50):
            # print(x)

            first_name = fake.first_name()
            last_name = fake.last_name()
            test_user = User(name=first_name + " " + last_name,
                             email=fake.email(),
                             date_of_birth=fake.date_of_birth(),
                             password=fake.password(),
                             username=fake.user_name(),
                             phone_number=fake.phone_number())

            session.add(test_user)
            print(test_user)
            session.commit()


def disperse_users_into_roles():
    print("$*(#^$*(#$^@#*$^@#$(@#^$*@(#^$@#^$*(^%$Y(*@#$^#@$(^")
    print("attendee or organiser")
    print("ratio of : just attendeee, just organiser, or both")
    fake = Faker()
    print("seed users")
    with rx.session() as session:
        session.exec(sqlalchemy.text("DELETE FROM Attendee"))
        session.exec(sqlalchemy.text("DELETE FROM Organiser"))
        # session.exec(sqlalchemy.text("VACUUM"))
        session.commit()
        users = session.query(User).all()
        for i, user in enumerate(users):
            print(f"User {i} -> DB ID: {user.id}")

            if i <= 35:
                print("just attendee")
                attendee = Attendee(user_id=user.id)
                session.add(attendee)
            elif i > 35 and i <= 45:
                print("both")
                attendee = Attendee(user_id=user.id)
                organiser = Organiser(user_id=user.id)
                session.add(attendee)
                session.add(organiser)
            else:
                print("just organiser")
                organiser = Organiser(user_id=user.id)
                session.add(organiser)

        session.commit()


def get_random_event_type():
    print("Bacon bacon bacon")
    print(len(EventType.list()))
    event_type_list = EventType.list()
    max = len(EventType.list())
    random.seed = datetime.time
    random_index = random.randrange(0, max)
    return event_type_list[random_index].value


def get_random_event_status():
    print("Bacon bacon bacon")
    print(len(EventType.list()))
    event_status_list = EventStatus.list()
    max = len(EventStatus.list())
    random.seed = datetime.time
    random_index = random.randrange(0, max)
    return event_status_list[random_index].value


def seed_events():
    seeded_event_type = get_random_event_type()
    seeded_event_status = get_random_event_status()
    print("events")
    with rx.session() as session:
        session.exec(sqlalchemy.text("DELETE FROM Event"))
        session.exec(sqlalchemy.text("DELETE FROM Perk"))
        session.exec(sqlalchemy.text("DELETE FROM Registration"))
        session.commit()
        fake = Faker()

        # for x in range(25):

        print("bacon bacon bacon")

        new_event = Event(name=str(fake.word()),
                          duration=0,
                          event_type=seeded_event_type,
                          date=fake.future_datetime(fake.date_this_year()),
                          location=str(fake.address()),
                          price_range_lowest=1,
                          price_range_highest=10,
                          description=fake.paragraph(1),
                          age_range="1",
                          attendees_num=1,
                          status=seeded_event_status,
                          capacity=1,
                          occupied_capacity=1
                          )
        session.add(new_event)
        session.commit()


def seed_one_attendee():
    with rx.session() as session:
        one_attendee = session.exec(Attendee.select()).first()
        one_event = session.exec(Event.select()).first()
        one_attendee.events.append(one_event)
        session.commit()
