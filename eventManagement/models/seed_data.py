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
        users = session.query(User).all()  # or use execute/text if needed
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
    # with rx.session() as session:
    #     # users = session.query(User).all()  # Get all users
    #     # result = session.execute(text('SELECT * FROM User'))
    #     # for user in result:
    #     #     print(user)
    #     result = session.execute(text('SELECT COUNT(*) FROM User'))
    #     # WHAT V
    #     count = result.scalar()
    #     print("$$$$$$$ " + str(count) + " $$$$$$$")
    #     for x in range(count):
    #         # user = session.query(User).filter(User.id == x).first()
    #         # result = session.execute(
    #         #     text("SELECT * FROM User WHERE id = :id"),
    #         #     {"id": x}
    #         # )
    #         print("*****")
    #         print(x)
    #         print("*****")
    #         # user = result.first()
    #         # print(user)
    #         if x <= 35:
    #             print("just attendee")
    #             attendee = Attendee(
    #                 user_id=x)
    #             session.add(attendee)
    #         elif x > 35 and x <= 45:
    #             print("both")
    #             attendee = Attendee(
    #                 user_id=x)
    #             session.add(attendee)
    #
    #             organiser = Organiser(
    #                 user_id=x)
    #             session.add(organiser)
    #         else:
    #             print("organiser")
    #             organiser = Organiser(
    #                 user_id=x)
    #             session.add(organiser)
    #     session.commit()


def seed_events():
    print("events")
