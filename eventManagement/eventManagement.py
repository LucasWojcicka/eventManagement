import reflex as rx
import sqlalchemy

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
    all_events = EventServices.get_all_events()
    # load_events = EventServices.LoadEvents()
    # load_events.load_all_events()
    return all_events


# @fastapi_app.get("/api/login_user")
# async def login_user(username, password):
#     from eventManagement.services.user_services import UserServices
#     login_user_def = UserServices.LogInUser
#     login_user_def.log_in_user()
#     # load_events = EventServices.LoadEvents()
#     # load_events.load_all_events()
#     return login_user_def.good_login_data


# @fastapi_app.get("/api/get_event")
# async def get_event(given_id):
#     from eventManagement.services.eventServices import EventServices
#     get_event_def = EventServices.GetEvent()
#     get_event_def.get_event_by_id()
#     return get_event_def.event_found


@fastapi_app.get("/api/get_event_by_id")
async def get_event(event_id: int):
    from eventManagement.services.eventServices import EventServices
    event = EventServices.get_event_by_id(event_id)
    return event


@fastapi_app.get("/api/get_attendee_events")
async def get_attended_events(attendee_id: int):
    from eventManagement.services.eventServices import EventServices
    attendee = EventServices.get_attending_events(attendee_id)
    return attendee
    # return events


@fastapi_app.get("/api/set_event_name")
async def get_attended_events(event_id: int, event_name: str):
    from eventManagement.services.eventServices import EventServices
    attendee = EventServices.set_event_name(event_id, event_name)
    return attendee
    # return events


@fastapi_app.get("/api/get_attenders_of_event")
async def get_attenders(event_id: int):
    from eventManagement.services.eventServices import EventServices
    attendee = EventServices.get_attenders(event_id)
    return attendee


@fastapi_app.get("/api/get_event_by_name")
async def get_event_by_name(name: str):
    from eventManagement.services.eventServices import EventServices
    return EventServices.get_event_by_name(name)


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
            rx.link(rx.button("dashboard", size="4"), href="/dashboard"),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


def login():
    return rx.container(
        header(),
        rx.container(
            rx.heading("Login", size="6", align="center")
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
        rx.text("about us", size="5"),
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
                            rx.link("Terms and Conditions", href="/about", size="2")
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


def dashboard():
    return rx.container(
        header(),
        rx.container(
            rx.grid(rx.foreach(rx.Var.range(12), lambda i: rx.card(f"Card {i + 1}", height="10vh"), ),
                    columns="3",
                    spacing="4",
                    width="100%",
                    )
        )
    )


def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="4", weight="medium"), href=url
    )


def header() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/logo.jpg",
                        width="2.25em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading(
                        "Zen Planner", size="7", weight="bold"
                    ),
                    align_items="center",
                ),
                rx.hstack(
                    navbar_link("Home", "/"),
                    navbar_link("About", "/about"),
                    navbar_link("Dashboard", "/dashboard"),
                    spacing="4",
                    align_items="center"
                ),
                rx.hstack(
                    rx.button(
                        "Sign Up",
                        size="3",
                        variant="outline",
                    ),
                    rx.dialog.root(
                        rx.dialog.trigger(rx.button("Log in", size="3")),
                        rx.dialog.content(
                            rx.dialog.title("Log in"),
                            rx.dialog.description(
                                "log in stuff",
                            ),
                            rx.dialog.close(
                                rx.button("Close", size="3"),
                            ),
                        ),
                    ),
                ),
                spacing="4",
                justify="between",
            ),
            justify="between",
            align_items="center",
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/logo.jpg",
                        width="2em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading(
                        "Reflex", size="6", weight="bold"
                    ),
                    align_items="center",
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon("menu", size=30)
                    ),
                    rx.menu.content(
                        rx.menu.item("Home"),
                        rx.menu.item("About"),
                        rx.menu.item("Dashboard"),
                        rx.menu.separator(),
                        rx.menu.item("Log in"),
                        rx.menu.item("Sign up"),
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        bg=rx.color("accent", 3),
        padding="1em",
        # position="fixed",
        # top="0px",
        # z_index="5",
        width="100%",
    )


# app = rx.App()
app = rx.App(api_transformer=fastapi_app)
app.add_all_routes_endpoint()
# TODO seed stuff

app.add_page(index)
app.add_page(dashboard, route="/dashboard")
app.add_page(login, route="/login")
app.add_page(aboutUs, route="/about")
app.add_page(createAccount, route="/createAccount")

from eventManagement.models.seed_data import seed_users
from eventManagement.models.seed_data import disperse_users_into_roles
from eventManagement.models.seed_data import seed_events
from eventManagement.models.seed_data import seed_one_attendee
from eventManagement.models.seed_data import seed_perks

#
seed_users()
disperse_users_into_roles()
seed_events()
seed_one_attendee()
seed_perks()
