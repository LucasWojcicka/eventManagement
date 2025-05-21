import reflex as rx

from eventManagement.models.seed_data import seed_users
from eventManagement.models.seed_data import disperse_users_into_roles
from eventManagement.models.seed_data import seed_events
from eventManagement.models.seed_data import seed_one_attendee
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

class LoginLogic(rx.State):
    form_data: dict = {}
    logged_in = False

    @rx.event
    def handleSubmit(self, formData: dict):
        # Handle the form submit.
        self.form_data = formData
        """Returned handshake is confirmed
        if login successful do"""

def index() -> rx.Component:
    # Index page
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

logged_in = False
def login_logic():
    if logged_in == False:
        return rx.hstack(
            rx.dialog.root(
                rx.dialog.trigger(rx.button("Create Account", size="3", variant="outline")),
                createAccountDialog()
            ),
            rx.dialog.root(
                rx.dialog.trigger(rx.button("Login", size="3")),
                loginDialog()
            ),
        ),
    else:
        return rx.avatar(src="/logo.jpg", fallback="LW", size="1"),

def aboutUs():
    return rx.container(
        header(),
        rx.text("about us", size = "5"),
    )

def dashboard():
    return rx.container(
        header(),
        rx.container(
            rx.grid(rx.foreach(rx.Var.range(12),lambda i: rx.card(f"Card {i + 1}", height="10vh"),),
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
        rx.color_mode.button(position="top-right"),
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
                login_logic(),
                # rx.hstack(
                #     rx.dialog.root(
                #         rx.dialog.trigger(rx.button("Create Account", size="3", variant="outline")),
                #         createAccountDialog()
                #     ),
                #     rx.dialog.root(
                #         rx.dialog.trigger(rx.button("Login", size="3")),
                #         loginDialog()
                #     ),
                # ),
                spacing="4",
                justify="between",
                align="center"
            ),
            justify="between",
            align_items="center",
        ),
        bg=rx.color("accent", 3),
        padding="1em",
        width="100%",
    )

def loginDialog():
    return rx.dialog.content(
        rx.dialog.title("Login"),
        rx.container(
            rx.vstack(
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="User Name",
                            name="user_name",
                        ),
                        rx.input(
                            placeholder="Password",
                            type="password",
                            name="pass_word",
                        ),
                        rx.button("Submit", type="submit"),
                        align="center",
                    ),
                    on_submit=LoginLogic.handleSubmit,
                    reset_on_submit=True,
                ),
            ),
        ),
        rx.dialog.close(
            rx.button("Close", size="3"),
        ),
    ),

def createAccountDialog():
    return rx.dialog.content(
        rx.dialog.title("Create Account"),
        rx.container(
            rx.vstack(
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="First Name",
                            name="first_name",
                        ),
                        rx.input(
                            placeholder="Last Name",
                            name="last_name",
                        ),
                        rx.input(
                            placeholder="User Name",
                            name="user_name",
                        ),
                        rx.input(
                            placeholder="Password",
                            type="password",
                            name="pass_word",
                        ),
                        rx.input(
                            placeholder="Email Address",
                            name="email_address",
                        ),
                        rx.hstack(
                            rx.checkbox("I agree to the", name="check"),
                            rx.link(
                                "Terms and Conditions",
                                href="/about",
                                size="2",
                                is_external=True)
                        ),
                        rx.button("Submit", type="submit"),
                        align="center",
                    ),
                    on_submit=LoginLogic.handleSubmit,
                    reset_on_submit=True,
                ),
            ),
        ),
        rx.dialog.close(
            rx.button("Close", size="3"),
        ),
    ),


app = rx.App(api_transformer=fastapi_app)
app.add_all_routes_endpoint()
# TODO seed stuff

app.add_page(index)
app.add_page(dashboard, route="/dashboard")
app.add_page(aboutUs, route="/about")

# seed_users()
# disperse_users_into_roles()
# seed_events()
# seed_one_attendee()
