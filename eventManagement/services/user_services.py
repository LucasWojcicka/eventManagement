import reflex as rx
import datetime

from eventManagement.models.attendee import Attendee
from eventManagement.models.event import Event
from eventManagement.models.organiser import Organiser
from eventManagement.models.user import User
from typing import Optional, List


class UserServices(rx.State):

    # attendee getters
    @staticmethod
    def get_all_attendees():
        with rx.session() as session:
            return session.exec(Attendee.select()).all()

    @staticmethod
    def get_attendee_by_id(attendee_id: int) -> Attendee | None:
        with (rx.session() as session):
            return session.exec(
                Attendee.select().where(Attendee.id == attendee_id)
            ).first()

    @staticmethod
    def get_attending_events(attendee_id: int):
        print("get attending events")
        with rx.session() as session:
            attendee = session.exec(Attendee.select().where(Attendee.id == attendee_id)).first()
            attending_events = attendee.events
            print(len(attending_events))
            return attending_events

    @staticmethod
    def get_attendees_base_user(attendee_id: int):
        with rx.session() as session:
            attendee = session.exec(Attendee.select().where(Attendee.id == attendee_id)).first()
            return session.exec(User.select().where(User.id == attendee.user_id))

    # organiser getters
    @staticmethod
    def get_all_organisers():
        with rx.session() as session:
            return session.exec(Organiser.select()).all()

    @staticmethod
    def get_organiser_by_id(organiser_id: int) -> Organiser | None:
        with rx.session() as session:
            return session.exec(Organiser.select().where(Organiser.id == organiser_id)).first()

    @staticmethod
    def get_organised_events(organiser_id: int):
        print("get attending events")
        with rx.session() as session:
            organiser = session.exec(Organiser.select().where(Organiser.id == organiser_id)).first()
            organised_events = organiser.events
            return organised_events

    @staticmethod
    def get_organisers_base_user(organiser_id: int):
        with rx.session() as session:
            organiser = session.exec(Organiser.select().where(Organiser.id == organiser_id)).first()
            return session.exec(User.select().where(User.id == organiser.user_id))

    # getters for user
    @staticmethod
    def get_user_by_id(user_id: int) -> User | None:
        with rx.session() as session:
            return session.exec(User.select().where(User.id == user_id)).first()

    @staticmethod
    def get_user_by_username(username: str) -> User | None:
        with rx.session() as session:
            return session.exec(User.select().where(User.username == username)).first()

    @staticmethod
    def get_organiser_from_base_user(user_id: int):
        with rx.session() as session:
            return session.exec(Organiser.select().where(Organiser.user_id == user_id)).first()

    @staticmethod
    def get_attendee_from_base_user(user_id: int):
        with rx.session() as session:
            return session.exec(Attendee.select().where(Attendee.user_id == user_id)).first()

    # setters
    @staticmethod
    def make_base_user(name: str, email: str, dob: datetime, password: str, username: str, phone_number: str):
        new_user = User(name=name,
                        email=email,
                        date_of_birth=dob,
                        password=password,
                        username=username,
                        phone_number=phone_number
                        )
        new_attendee_from_user = Attendee(
            user_id=new_user.id
        )
        new_organiser_from_user = Organiser(
            user_id=new_user.id
        )
        with rx.session() as session:
            # TODO not allow user to make account if phone-number or email are taken
            exists = session.exec(User.select().where(User.username == username)).first()
            if (exists is not None):
                return False;
            else:
                session.add(new_user)
                session.add(new_attendee_from_user)
                session.add(new_organiser_from_user)
                session.commit()
                return True

    @staticmethod
    def set_user_name(user_id: int, username: str):
        with rx.session() as session:
            user = UserServices.get_user_by_id(user_id)
            before = user.name
            user.name = username
            print(before + " -> " + user.name)
            session.add(user)
            session.commit()

    @staticmethod
    def set_email(user_id: int, email: str):
        with rx.session() as session:
            user = UserServices.get_user_by_id(user_id)
            before = user.email
            user.email = email
            print(before + " -> " + user.email)
            session.add(user)
            session.commit()

    @staticmethod
    def set_phone(user_id: int, phone: str):
        with rx.session() as session:
            user = UserServices.get_user_by_id(user_id)
            before = user.phone_number
            user.phone_number = phone
            print(before + " -> " + user.phone_number)
            session.add(user)
            session.commit()

    # TODO password protections
    @staticmethod
    def set_password(user_id: int, password: str):
        with rx.session() as session:
            user = UserServices.get_user_by_id(user_id)
            before = user.password
            user.password = password
            print(before + " -> " + user.password)
            session.add(user)
            session.commit()

    # user actions

    @staticmethod
    def login_user(username: str, password: str):
        with rx.session() as session:
            user = session.exec(User.select().where(User.username == username and User.password == password)).first()
            if (user is not None):
                print("nuh uh")
                return True
            else:
                print("rklsdhfsd")
                return False
# login user, make event, unmake-event, attend event, un-attend event

# class AddUser(rx.State):
#     name: str
#     email: str
#     date_of_birth: datetime.date
#     password: str
#     username: str
#     phone_number: str
#
#     @rx.event
#     def add_user(self):
#         with rx.session() as session:
#             session.add(
#                 User(
#                     name=self.name,
#                     email=self.email,
#                     date_of_birth=self.date_of_birth,
#                     password=self.password,
#                     username=self.username,
#                     phone_number=self.phone_number
#                 )
#             )
#             session.commit()
#
# # works V
# class LoadUsers():
#     users: list[User]
#
#     def load_all_users(self):
#         with rx.session() as session:
#             self.users = session.exec(User.select()).all()
#
# class ChangeUsername(rx.State):
#     id: int
#     username: str
#
#     @rx.event
#     def change_username(self):
#         with rx.session() as session:
#             user = session.exec(
#                 User.select().where(
#                     (User.id == self.id)
#                 )
#             ).first()
#             user.username = self.username
#             session.add(user)
#             session.commit()
#
# class ChangeEmail(rx.State):
#     id: int
#     email: str
#
#     @rx.event
#     def change_email(self):
#         with rx.session() as session:
#             user = session.exec(
#                 User.select().where(
#                     (User.id == self.id)
#                 )
#             ).first()
#             user.email = self.email
#             session.add(user)
#             session.commit()
#
# #             TODO protection, authentication etc etc
# class ChangePassword(rx.State):
#     id: int
#     password: str
#
#     @rx.event
#     def change_password(self):
#         with rx.session() as session:
#             user = session.exec(
#                 User.select().where(
#                     (User.id == self.id)
#                 )
#             ).first()
#             user.password = self.password
#             session.add(user)
#             session.commit()
#
# class ChangePhoneNumber(rx.State):
#     id: int
#     phone_number: str
#
#     @rx.event
#     def change_phone_number(self):
#         with rx.session() as session:
#             user = session.exec(
#                 User.select().where(
#                     (User.id == self.id)
#                 )
#             ).first()
#             user.phone_number = self.phone_number
#             session.add(user)
#             session.commit()
#
# # log-in user
# class LogInUser(rx.State):
#     # id: int
#     username: str
#     password: str
#     good_login_data: bool = False
#
#     @rx.event
#     def log_in_user(self):
#         with rx.session() as session:
#             print("meow")
#             # user = session.exec(
#             #     User.select().where(
#             #         (User.username == self.username and User.password == self.password)
#             #     )
#             # ).first()
#             # if (user != None):
#             #     self.good_login_data = True
#             #     print("bacon bacon bacon")
#         # return self.good_login_data
#         # return user
#
# # get user-organiser-portal
# # get user-attendee-portal
#
# # attend_event
#
# class AttendEvent(rx.State):
#     id: int
#     event_to_attend_id: int
#
#     @rx.event
#     def user_attend_event(self):
#         with rx.session() as session:
#             event = session.exec(Event.select.where(Event.id == self.event_to_attend_id)).first()
#             attendee = session.exec(Attendee.select().where(Attendee.id == self.id))
#
#         #     user = session.exec(
#         #         User.select().where(
#         #             (User.username == self.username and User.password == self.password)
#         #         )
#         #     ).first()
#         #     if (user != None):
#         #         self.good_login_data = True
#         #         print("bacon bacon bacon")
#         # return self.good_login_data
