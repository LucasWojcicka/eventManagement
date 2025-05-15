import reflex as rx

import eventManagement
from rxconfig import config
# from eventManagement.models import User, Attendee, Organiser, Event

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


@fastapi_app.get("/api/events")
async def get_events():
    from eventManagement.services.eventServices import EventServices
    load_events = EventServices.LoadEvents()
    load_events.load_all_events()
    return load_events.events

class FormState(rx.State):
    form_data: dict = {}

    @rx.event
    def handleSubmit(self, formData: dict):
        """Handle the form submit."""
        self.form_data = formData

def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Event Management Application TEST!", size="9"),
            rx.text("Welcome", size="5"),
            rx.link(rx.button("login", size="4"), href="/login"),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )

def login():
    return rx.container(
        header(),
        rx.container(
            rx.heading("Login Page", size="6", align="center")
        ),
        rx.container(
            rx.vstack(
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="User Name",
                            name="userName",
                        ),
                        rx.input(
                            placeholder="Email Address",
                            name="emailAddress",
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

def aboutUs():
    return rx.container(
        header(),
        rx.text("about us", size = "5"),
    )

def createAccount():
        return rx.container(
        header(),
        rx.container(
            rx.heading("Create Account", size="6", align="center")
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
                            placeholder="User Name",
                            name="userName",
                        ),
                        rx.input(
                            placeholder="Email Address",
                            name="emailAddress",
                        ),
                        rx.hstack(
                            rx.checkbox("I agree to the", name="check"),
                            rx.link("Terms and Conditions", href="/about", size = "2")
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

def header():
    return rx.flex(
        rx.card(rx.link("home", href = "/")),
        rx.card(rx.link("login", href = "/login")),
        rx.card(rx.link("create account", href = "/createAccount")),
        rx.card(rx.link("about", href = "/about")),
        rx.color_mode.button(position="top-right"),
        spacing="2",
        width="100%",
        justify="center",
    )

# app = rx.App()
app = rx.App(api_transformer=fastapi_app)
app.add_all_routes_endpoint()
# TODO seed stuff

app.add_page(index)
app.add_page(login, route="/login")
app.add_page(aboutUs, route="/about")
app.add_page(createAccount, route="/createAccount")

from eventManagement.models.seed_data import seed_users
from eventManagement.models.seed_data import disperse_users_into_roles
from eventManagement.models.seed_data import seed_events
from eventManagement.models.seed_data import seed_one_attendee

# seed_users()
# disperse_users_into_roles()
# seed_events()
# seed_one_attendee()
