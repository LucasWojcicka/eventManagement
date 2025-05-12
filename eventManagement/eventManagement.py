import reflex as rx

import eventManagement
from rxconfig import config
from eventManagement.models import User, Attendee, Organiser, Event

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer


class State(rx.State):
    """The app state."""

    ...


fastapi_app = FastAPI(title="My API")


# Add routes to the FastAPI app
@fastapi_app.get("/api/items")
async def get_items():
    return "meow"


@fastapi_app.get("/api/users")
async def get_users():
    from eventManagement.services.user_services import UserServices
    load_users = UserServices.LoadUsers()
    load_users.load_all_users()
    return load_users.users


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Event Management Application TEST!", size="9"),
            rx.text("Welcome", size="5"),
            rx.link(rx.button("login", size="4"), href="/form"),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


class FormState(rx.State):
    form_data: dict = {}

    @rx.event
    def handleSubmit(self, formData: dict):
        """Handle the form submit."""
        self.form_data = formData


def form_example():
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.container(
            rx.heading("Login Page", size="6", align="center")
        ),
        rx.container(
            rx.vstack(
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="First Name",
                            name="firstName",
                        ),
                        rx.input(
                            placeholder="Last Name",
                            name="lastName",
                        ),
                        rx.input(
                            placeholder="Email Address",
                            name="emailAddress",
                        ),
                        rx.hstack(
                            rx.checkbox("I agree to the Terms and Conditions", name="check"),
                        ),
                        rx.button("Submit", type="submit"),
                        align="center",
                    ),
                    on_submit=FormState.handleSubmit,
                    reset_on_submit=True,
                ),
            ),
        ),
    )


# app = rx.App()
app = rx.App(api_transformer=fastapi_app)
app.add_all_routes_endpoint()
# TODO seed stuff
app.add_page(index)

app.add_page(form_example, route="/form")

from eventManagement.models.seed_data import seed_users
from eventManagement.models.seed_data import disperse_users_into_roles
from eventManagement.models.seed_data import seed_events

#
seed_users()
disperse_users_into_roles()
seed_events()
