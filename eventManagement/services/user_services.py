import reflex as rx
import datetime

from eventManagement.models.attendee import Attendee
from eventManagement.models.event import Event, Registration
from eventManagement.models.organiser import Organiser
from eventManagement.models.user import User
from eventManagement.services.eventServices import EventServices


class UserServices(rx.State):

    """
    getters for attendees
    """
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
    def organise_event(user_id: int, event: Event):
        with rx.session() as session:
            organiser = session.exec(Organiser.select().where(Organiser.user_id == user_id)).first()
            organiser.events.append(event)
            session.commit()

    @staticmethod
    def make_organiser(base_user_id: int):
        with rx.session() as session:
            organiser = Organiser(user_id=base_user_id)
            session.add(organiser)
            session.commit()

    @staticmethod
    def make_attendee(base_user_id: int):
        with rx.session() as session:
            attendee = Attendee(user_id=base_user_id)
            session.add(attendee)

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
    def get_user_registrations(user_id: int):
        with rx.session() as session:
            all_regos = session.exec(Registration.select()).all()
            user_regos = []
            for rego in all_regos:
                if rego.user_id == user_id:
                    user_regos.append(rego)
            return user_regos

    @staticmethod
    def get_user_registrations_for_event(user_id: int, event_id : int):
        with rx.session() as session:
            all_regos = session.exec(Registration.select()).all()
            user_regos = []
            for rego in all_regos:
                if rego.user_id == user_id and rego.event_id == event_id:
                    user_regos.append(rego)
            return user_regos

    @staticmethod
    def registration_representer(registrations: list):
        readable_registrations = []

        for rego in registrations:
            readable = {
                "id" : rego.id,
                "price" : rego.price,
                "approved" : rego.approved,
                "user_id" : rego.user_id,
                "event_id" : rego.event_id,
                "perk_id" : rego.perk_id,
                "registration_date" : rego.registration_date,
                "approved_date" : rego.approved_date,
                "user_name" : UserServices.get_user_by_id(rego.user_id).name,
                "event_name" : EventServices.get_event_by_id(rego.event_id).name,
                "event_type" : EventServices.get_event_by_id(rego.event_id).event_type,
                "event_status" : EventServices.get_event_by_id(rego.event_id).status,
                "event_date" : EventServices.get_event_by_id(rego.event_id).date,
                "perk_name" : EventServices.get_perk_by_id(rego.perk_id).name,
            }
            readable_registrations.append(readable)

        return readable_registrations



    @staticmethod
    def get_attenders(event_id: int):
        print("get attenders of event")
        with rx.session() as session:
            all_attendees = session.exec(Attendee.select()).all()
            matching_users = []

            for attendee in all_attendees:
                for event in attendee.events:
                    if event.id == event_id:
                        user = session.exec(User.select().where(User.id == attendee.user_id)).first()
                        if user:
                            matching_users.append(user)
                        break

            print(f"Found {len(matching_users)} users attending event {event_id}")
            return matching_users

    @staticmethod
    def get_organised_events(organiser_id: int):
        print("get ORGANISED events")
        with rx.session() as session:
            organiser = session.exec(Organiser.select().where(Organiser.id == organiser_id)).first()
            organised_events = organiser.events
            print(len(organised_events))
            return organised_events

    @staticmethod
    def get_organisers_base_user(organiser_id: int):
        with rx.session() as session:
            organiser = session.exec(Organiser.select().where(Organiser.id == organiser_id)).first()
            return session.exec(User.select().where(User.id == organiser.user_id))

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

    @staticmethod
    def get_user_from_username(username : str):
        with rx.session() as session:
            return session.exec(User.select().where(User.username == username)).first()
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
                # return False;
                return None;
            else:
                session.add(new_user)
                session.add(new_attendee_from_user)
                session.add(new_organiser_from_user)
                session.commit()
                user = UserServices.get_user_from_username(new_user.username)
                # return True
                # return new_user
                return user

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
                return user
            else:
                print("rklsdhfsd")
                return None
