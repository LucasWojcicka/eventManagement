# import datetime
#
# import reflex as rx
# import sqlalchemy
# from sqlmodel import Session
# from faker import Faker
#
# from event_management.model.user import User
# # from event_management.model.attendee import Attendee
# # from event_management.model.organiser import Organiser
# # from event_management.model.event import Event
#
# from faker.providers import DynamicProvider
#
# event_name_provider = DynamicProvider(
#     provider_name="event_name",
#     elements=["Neon Mirage Concert", "Echo Drift Concert", "Midnight Arcadia Concert", "Sonic Bloom Concert",
#               "Velvet Pulse Concert", "Crystal Static Concert", "Superintergalactic Concert", "Dreamforge Concert",
#               "Luna Loop Concert", "Bassfield Concert", "Quantum Verge Conference", "Catalyst Theory Conference",
#               "Infinite Thread Conference", "Nova Stack Conference", "MetaCraft Conference", "CodeChroma Conference",
#               "Altisphere Conference", "MindSync Conference", "Circuit Summit Conference", "Ethereal Vision Conference",
#               "Lumina Flow Exhibition", "Visual Bloom Exhibition", "ModuloForm Exhibition", "Spectrum Grid Exhibition",
#               "Temporal Canvas Exhibition", "Parallax Vault Exhibition", "ObjectArc Exhibition",
#               "VantaSpace Exhibition", "Neon Archive Exhibition", "RetroConstruct Exhibition",
#               "Arcadia Exchange Networking", "Nexus Pulse Networking", "EchoLink Networking",
#               "Fusion Thread Networking", "NightBloom Networking", "BrightLoop Networking", "Velvet Circuit Networking",
#               "CrossCurrent Networking", "ForgeZone Networking", "Uplink Union Networking"],
# )
#
#
# # engine = rx.utils.get_db_engine()
# # engine = rx.utils.get_engine()
#
#
# def make_users():
#     fake = Faker()
#     with rx.session() as session:
#         existing_data = session.exec(User.select()).first()
#         if existing_data:
#             print(f"already data, pass: {existing_data}")
#             # session.exec(sqlalchemy.text("DELETE FROM User"))
#             # session.commit()
#             # return
#         else:
#             for x in range(50):
#                 first_name = fake.first_name()
#                 last_name = fake.last_name()
#                 test_user = User(name=first_name + " " + last_name,
#                                  email=fake.email(),
#                                  date_of_birth=fake.date_of_birth(),
#                                  password=fake.password(),
#                                  username=fake.user_name(),
#                                  phone_number=fake.phone_number())
#
#                 session.add(test_user)
#                 # if (x % 5 == 0):
#                 #     test_organiser = Organiser(user=test_user)
#                 #     session.add(test_organiser)
#                 # else:
#                 #     test_attendee = Attendee(user=test_user)
#                 #     session.add(test_attendee)
#             session.commit()
#
#
# # def make_events():
# #     fake = Faker()
# #     fake.add_provider(event_name_provider)
# #     with rx.session() as session:
# #         existing_data = session.exec(Event.select()).first()
# #         if existing_data:
# #             print(f"already data, pass: {existing_data}")
# #             return
# #         else:
# #             for x in range(50):
# #                 test_event = Event(name=fake.event_name(),
# #                                    duration=(x in range(1, 6)),
# #                                    # event_type=Event_Type,
# #                                    date=fake.future_datetime(),
# #                                    location=fake.street_address_with_county(),
# #                                    price_range_lowest=(x in range(0, 500)),
# #                                    price_range_highest=(x in range(test_event.price_range_lowest,
# #                                                                    test_event.price_range_lowest + 500)),
# #                                    description=fake.opera()
# #
# #                                    )
# #
# #                 session.add(test_event)
# #             session.commit()
# #
# #     # name: str
# #     # duration: int
# #     # event_type: EventType
# #     # date: datetime.date
# #     # location: str
# #     # price_range_lowest: int
# #     # price_range_highest: int
# #     # description: str
# #     # age_range: str
# #     # event_id: int
# #     # attendees_num: int
# #     # attendees: List[Attendee]
# #     # registration_types: List[Registration]
# #     # available_perks: List[Perks]
# #     # status: EventStatus
# #     # capacity: int
# #     # occupied_capacity: int
# #     return
#
#
# def make_all():
#     make_users()

import datetime

import reflex as rx
import sqlalchemy
from sqlmodel import Session
from faker import Faker

from eventManagement.models.user import User
from eventManagement.models.event import Event
from eventManagement.models.attendee import Attendee
from eventManagement.models.organiser import Organiser


# def make_users():
#     fake = Faker()
#     with rx.session() as session:
#         existing_data = session.exec(User.select()).first()
#         if existing_data:
#             print(f"already data, pass: {existing_data}")
#             # session.exec(sqlalchemy.text("DELETE FROM User"))
#             # session.commit()
#             # return
#         else:
#             for x in range(50):
#                 first_name = fake.first_name()
#                 last_name = fake.last_name()
#                 test_user = User(name=first_name + " " + last_name,
#                                  email=fake.email(),
#                                  date_of_birth=fake.date_of_birth(),
#                                  password=fake.password(),
#                                  username=fake.user_name(),
#                                  phone_number=fake.phone_number())
#
#                 session.add(test_user)
#                 # if (x % 5 == 0):
#                 #     test_organiser = Organiser(user=test_user)
#                 #     session.add(test_organiser)
#                 # else:
#                 #     test_attendee = Attendee(user=test_user)
#                 #     session.add(test_attendee)
#             session.commit()

def seed_users():
    print("seed users")
    fake = Faker()
    with rx.session() as session:
        # existing_data = session.exec(User.select()).first()
        # if existing_data:
        #     print(f"already data, pass: {existing_data}")
        #     # session.exec(sqlalchemy.text("DELETE FROM User"))
        #     # session.exec(sqlalchemy.text("VACUUM"))
        #     # session.commit()
        #     # return
        # else:
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
        session.commit()

def  disperse_users_into_roles():
    print("attendee or organiser")
    print("ratio of : just attendeee, just organiser, or both")
