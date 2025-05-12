import datetime

import reflex as rx
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlmodel import Session
from faker import Faker

from eventManagement.models.user import User
from eventManagement.models.event import Event
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

def seed_events():
    print("events")
    for x in range(25):
        with rx.session() as session:
            session.exec(sqlalchemy.text("DELETE FROM Event"))
            session.exec(sqlalchemy.text("DELETE FROM Perks"))
            session.exec(sqlalchemy.text("DELETE FROM Registration"))
            session.commit()



