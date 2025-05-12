import reflex as rx

from eventManagement.models.user import User
from typing import Optional, List


class UserServices:
    class AddUser(rx.State):
        username: str
        email: str

        @rx.event
        def add_user(self):
            with rx.session() as session:
                session.add(
                    User(
                        username=self.username, email=self.email
                    )
                )
                session.commit()

    # works V
    class LoadUsers():
        users: list[User]
        def load_all_users(self):
            with rx.session() as session:
                self.users = session.exec(User.select()).all()

