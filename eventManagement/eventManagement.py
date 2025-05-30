import datetime

import reflex as rx
import sqlalchemy

from eventManagement.models.event import Event
from eventManagement.models.seed_data import seed_users, seed_perks
from eventManagement.models.seed_data import disperse_users_into_roles
from eventManagement.models.seed_data import seed_events
from eventManagement.models.seed_data import seed_one_attendee
from eventManagement.models.user import User
from eventManagement.services.eventServices import EventServices
from eventManagement.services.user_services import UserServices
from rxconfig import config
# from eventManagement.models import User, Attendee, Organiser, Event
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

fastapi_app = FastAPI(title="My API")


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


@fastapi_app.get("/api/get_user_by_id")
async def get_user_by_id(user_id: int):
    from eventManagement.services.user_services import UserServices
    user = UserServices.get_user_by_id(user_id)
    return user


@fastapi_app.get("/api/get_user_by_username")
async def get_user_by_id(username: str):
    from eventManagement.services.user_services import UserServices
    user = UserServices.get_user_by_username(username)
    return user


@fastapi_app.get("/api/get_attendee_events")
async def get_attended_events(attendee_id: int):
    from eventManagement.services.eventServices import EventServices
    attendee = EventServices.get_attending_events(attendee_id)
    return attendee
    # return events


@fastapi_app.get("/api/get_event_perks")
async def get_event_perks(event_id: int):
    from eventManagement.services.eventServices import EventServices
    perks = EventServices.get_event_perks_from_event_id(event_id)
    return perks


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


class AppState(rx.State):
    """The app state."""
    current_user_id: int = -1
    selected_user: dict | None = None
    # current_user: User
    ...

    @rx.event
    async def fetch_current_user(self):
        from eventManagement.services.user_services import UserServices
        if self.current_user_id:
            user = UserServices.get_user_by_id(self.current_user_id)
            if user:
                self.selected_user = user.to_dict()

    @rx.event
    def setUser(self, user_id: int):
        self.current_user_id = user_id
        print(AppState.current_user_id)
    # if(self.current_user_id != -1):
    #     self.current_user = UserServices.get_user_by_id(self.current_user_id)


# @rx.event
# def fetch_current_user(self):
#     from eventManagement.services.user_services import UserServices
#
#     if self.current_user_id:
#         user = UserServices.get_user_by_id(self.current_user_id)
#         if user:
#             self.selected_user = user.to_dict()


# fastapi_app = FastAPI(title="My API")


# Add routes to the FastAPI app


class DashboardState(AppState):
    events: list[dict] = []
    selected_event: dict | None = None

    @rx.event
    async def load_events(self):
        from eventManagement.services.eventServices import EventServices
        events_list = EventServices.get_all_events()
        self.events = [event.to_dict() for event in events_list]

    @rx.event
    async def fetch_and_redirect(self, event_id: int):
        from eventManagement.services.eventServices import EventServices
        event = EventServices.get_event_by_id(event_id)
        if event:
            self.selected_event = event.to_dict()
            return rx.redirect("/event-detail")


class LoginLogic(AppState):
    form_data: dict = {}

    @rx.event
    def handleSubmit(self, formData: dict):
        print("bacon bacon bacon")
        username = formData.get("user_name")
        password = formData.get("pass_word")
        print(username + " " + password)
        correctDetails = UserServices.login_user(username, password)
        print(correctDetails)
        if (correctDetails == True):
            user = UserServices.get_user_by_username(username)
            print(user)
            user_id = user.id
            # setUser(AppState, user_id)
            self.current_user_id = user_id
            # AppState.current_user_id = user_id
            # LoginLogic.father_state.setUser(State, user_id)
            # rx.session().set("user_id", user.id)
            print(AppState.current_user_id)
            yield rx.redirect("/home")
            # rx.navigate("/home", user_id=AppState.current_user_id)

        print(AppState.current_user_id)


class CreateAccount(AppState):
    form_data: dict = {}

    @rx.event
    def handleSubmit(self, formData: dict):
        print("bacon bacon bacon")
        username = formData.get("user_name")
        password = formData.get("pass_word")
        name = formData.get("first_name") + " " + formData.get("last_name")
        email = formData.get("email_address")
        birth = formData.get("date_of_birth")
        phone = formData.get("phone_number")
        correctDetails = UserServices.make_base_user(name, email, birth, password, username, phone)
        print(correctDetails)
        if (correctDetails == True):
            print("good made user")
            user = UserServices.get_user_by_username(username)
            print(user)
            user_id = user.id
            # setUser(AppState, user_id)
            self.current_user_id = user_id

            yield rx.redirect("/home/")
            # LoginLogic.handleSubmit(self,formData)
        #     user = UserServices.get_user_by_id(username)
        #     State.user_id = user.id
        #     print(State.user_id)
        #
        # print(State.user_id)


# def index() -> rx.Component:
#     # Index page
#     return rx.container(
#         rx.color_mode.button(position="top-right"),
#         rx.vstack(
#             rx.heading("Welcome To Zen Planner! Where anyone can organise an Event!", size="9"),
#             rx.text("Welcome", size="5"),
#             rx.link(rx.button("Log in", size="4"), href="/dashboard"),
#             rx.link(rx.button("Create Account", size="4"), href="/dashboard"),
#             spacing="5",
#             justify="center",
#             min_height="85vh",
#         ),
#     )
def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome To Zen Planner!", size="9"),
            rx.text("Where anyone can organise an event!", size="5"),
            rx.hstack(
                rx.dialog.root(
                    rx.dialog.trigger(rx.button("Create Account", size="4", variant="outline")),
                    createAccountDialog()
                ),
                rx.dialog.root(
                    rx.dialog.trigger(rx.button("Login", size="4")),
                    loginDialog()
                ),
                spacing="4"
            ),
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
        return rx.avatar(src="/logo.jpg", fallback="LW", size="3"),


def aboutUs():
    return rx.container(
        header(),
        rx.text("about us", size="5"),
    )


def pureTesting():
    return rx.container(
        header(),
        rx.text("pure testing", size="5"),
    )


# def dashboard():
#         return rx.container(
#             header(),
#             rx.container(
#                 rx.grid(rx.foreach(rx.Var.range(12), lambda i: rx.card(f"Card {i + 1}", height="10vh"), ),
#                         columns="3",
#                         spacing="4",
#                         width="100%",
#                         )
#             )
#         )
@rx.page(on_load=DashboardState.load_events)
def dashboard():
    DashboardState.load_events()

    return rx.container(
        header(),
        rx.container(
            rx.grid(
                rx.foreach(
                    DashboardState.events,
                    # lambda event: rx.card(
                    #     rx.text(event["name"]),rx.text(event["event_type"]),
                    #     height="10vh"
                    # ),
                    lambda event: rx.card(
                        rx.vstack(
                            rx.text(f"{event['name']} {event['event_type']}", font_weight="bold"),
                            rx.text(event["location"], font_style="italic"),
                            # rx.text(event["date"].strftime("%d/%m/%Y - %H:%M"), font_weight="bold"),
                            rx.text(event["age_range"]),
                        ),
                        height="25vh",
                        on_click=lambda e=event: DashboardState.fetch_and_redirect(e["id"])
                    )
                ),
                columns="3",
                spacing="4",
                width="100%",
            )
        ),
    )


# @rx.page(route="/event-detail")
# def event_detail():
#     event = DashboardState.selected_event
#
#     return rx.container(
#         rx.heading(event["name"]),
#         rx.text(f"Type: {event['event_type']}"),
#         rx.text(f"Location: {event['location']}"),
#         rx.text(f"Date: {event['date']}"),
#         rx.text(f"Age Range: {event['age_range']}"),
#         rx.button("Back to Dashboard", on_click=rx.redirect("/dashboard")),
#         padding="4",
#     )

@rx.page(route="/event-detail")
def event_detail():
    event = DashboardState.selected_event

    return rx.container(
        rx.heading(event["name"]),
        rx.text(f"Type: {event['event_type']}"),
        rx.text(f"Location: {event['location']}"),
        rx.text(f"Date: {event['date']}"),
        rx.text(f"Age Range: {event['age_range']}"),
        rx.button("Back to Dashboard", on_click=rx.redirect("/dashboard")),
        padding="4",
    )


# @rx.page(route="/home")
# # def user_home_page():
# #     # user_id = int(AppState.current_user_id)
# #     # user = UserServices.get_user_by_id(AppState.current_user_id)
# #     # print(AppState.current_user_id)
# #     # print(UserServices.get_user_by_id(AppState.current_user_id).name)
# #     # print(AppState.current_user)
# #
# #     print("BALLLS")
# #     print(AppState.current_user_id)
# #     return rx.container(
# #         # rx.heading(str(user.id)),
# #         rx.heading(AppState.current_user_id),
# #         # rx.text(f"Welcome {user.name} !"),
# #         padding="4",
# #     )
@rx.page(route="/home", on_load=AppState.fetch_current_user)
def user_home_page():
    return rx.container(
        rx.heading("User Home"),
        rx.cond(
            AppState.selected_user,
            rx.vstack(
                rx.text(f"Welcome {AppState.selected_user['name']}!"),
                rx.text(f"Email: {AppState.selected_user['email']}"),
                rx.text(f"Username: {AppState.selected_user['username']}"),
                rx.text(f"id: {AppState.selected_user['id']}"),
            ),
            rx.text("Loading user data...")
        ),
        padding="4",
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
                    navbar_link("Purely Testing", "/testing"),
                    spacing="4",
                    align_items="center",
                    justify="center"
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
                spacing="1",
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
                        rx.input(
                            placeholder="Phone Number",
                            name="phone_number",
                        ),
                        rx.input(
                            type="date",
                            name="date_of_birth",
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
                    on_submit=CreateAccount.handleSubmit,
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
app.add_page(pureTesting(), route="/testing")

#
seed_users()
disperse_users_into_roles()
seed_events()
seed_one_attendee()
seed_perks()

# TODO
# organiser portal
# -> make event
# -> see made events
# -> array of registration per event
# --> approve / disapporve registration

# attender portal
# -> search event by term
# -> perks on event
# -> book tickets and ticket perks
# -> or approve reigstration, get tickets
