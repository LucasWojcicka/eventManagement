import reflex as rx
import datetime
from eventManagement.models.user import User
from typing import Optional, List


class UserServices(rx.State):
    class AddUser(rx.State):
        name: str
        email: str
        date_of_birth: datetime.date
        password: str
        username: str
        phone_number: str

        @rx.event
        def add_user(self):
            with rx.session() as session:
                session.add(
                    User(
                        name=self.name,
                        email=self.email,
                        date_of_birth=self.date_of_birth,
                        password=self.password,
                        username=self.username,
                        phone_number=self.phone_number
                    )
                )
                session.commit()

    # works V
    class LoadUsers():
        users: list[User]

        def load_all_users(self):
            with rx.session() as session:
                self.users = session.exec(User.select()).all()

    class ChangeUsername(rx.State):
        id: int
        username: str

        @rx.event
        def change_username(self):
            with rx.session() as session:
                user = session.exec(
                    User.select().where(
                        (User.id == self.id)
                    )
                ).first()
                user.username = self.username
                session.add(user)
                session.commit()

    class ChangeEmail(rx.State):
        id: int
        email: str

        @rx.event
        def change_email(self):
            with rx.session() as session:
                user = session.exec(
                    User.select().where(
                        (User.id == self.id)
                    )
                ).first()
                user.email = self.email
                session.add(user)
                session.commit()

    #             TODO protection, authentication etc etc
    class ChangePassword(rx.State):
        id: int
        password: str

        @rx.event
        def change_password(self):
            with rx.session() as session:
                user = session.exec(
                    User.select().where(
                        (User.id == self.id)
                    )
                ).first()
                user.password = self.password
                session.add(user)
                session.commit()

    class ChangePhoneNumber(rx.State):
        id: int
        phone_number: str

        @rx.event
        def change_phone_number(self):
            with rx.session() as session:
                user = session.exec(
                    User.select().where(
                        (User.id == self.id)
                    )
                ).first()
                user.phone_number = self.phone_number
                session.add(user)
                session.commit()
