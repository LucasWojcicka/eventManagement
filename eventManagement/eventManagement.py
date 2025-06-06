from datetime import datetime
import reflex as rx
from eventManagement.models.event import Event, EventType, EventStatus, Perk
from eventManagement.models.seed_data import seed_users, seed_perks, seed_all_attendees, seed_all_organisers, \
    seed_all_registrations
from eventManagement.models.seed_data import disperse_users_into_roles
from eventManagement.models.seed_data import seed_events
from eventManagement.models.seed_data import seed_one_attendee
from eventManagement.services.eventServices import EventServices
from eventManagement.services.user_services import UserServices

from fastapi import FastAPI, Depends

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
    return all_events


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


@fastapi_app.get("/api/get_attendee_by_user_id")
async def get_user_by_id(user_id: int):
    from eventManagement.services.user_services import UserServices
    attendee = UserServices.get_attendee_from_base_user(user_id)
    return attendee


@fastapi_app.get("/api/get_user_by_username")
async def get_user_by_id(username: str):
    from eventManagement.services.user_services import UserServices
    user = UserServices.get_user_by_username(username)
    return user


@fastapi_app.get("/api/get_attendee_events")
async def get_attended_events(attendee_id: int):
    from eventManagement.services.user_services import UserServices
    attendee = UserServices.get_attending_events(attendee_id)
    # return attendee.events
    # return events


@fastapi_app.get("/api/get_organised_events")
async def get_organised_events(base_user_id: int):
    from eventManagement.services.user_services import UserServices
    organiser = UserServices.get_organiser_from_base_user(base_user_id)
    return organiser.events
    # return events


@fastapi_app.get("/api/get_event_perks")
async def get_event_perks(event_id: int):
    from eventManagement.services.eventServices import EventServices
    perks = EventServices.get_event_perks_from_event_id(event_id)
    return perks


# TODO Edit event (placeholders not values) | Must make perk to make event

@fastapi_app.get("/api/set_event_name")
async def get_attended_events(event_id: int, event_name: str):
    from eventManagement.services.eventServices import EventServices
    attendee = EventServices.set_event_name(event_id, event_name)
    return attendee
    # return events


@fastapi_app.get("/api/make_event")
async def make_event(name: str, duration: int, event_type: str, date: datetime, location: str, price_low: int,
                     price_high: int, desc: str, age: str, attendee: int, status: str, capacity: int, occupied: int):
    from eventManagement.services.eventServices import EventServices
    # EventServices.create_event(name, duration, event_type, datetime.now(), location, price_low, price_high, desc, age,
    #                            status, capacity)
    # return attendee
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
    """The app state.
    current_user_id : The id of the user currently logged in
    selected_user : The current user's details, represented as a dictionary. Dictionaries are
    used instead of instances of objects as only primitive objects are able to be used in Reflex, and
    Dictionaries are easier to pass
    """
    current_user_id: int = -1
    selected_user: dict | None = None
    ...

    @rx.event
    async def fetch_current_user(self):
        """
        get current user object using current_user_id and set returned object as selected_user
        """
        from eventManagement.services.user_services import UserServices
        if self.current_user_id:
            user = UserServices.get_user_by_id(self.current_user_id)
            if user:
                self.selected_user = user.to_dict()

    @rx.event
    async def get_attendee_from_base_user(self):
        from eventManagement.services.user_services import UserServices
        if self.current_user_id:
            attendee = UserServices.get_attendee_from_base_user(self.current_user_id)
            if attendee:
                self.selected_user = attendee.to_dict()
                # self.attendee_from_user = attendee

    @rx.event
    def setUser(self, user_id: int):
        self.current_user_id = user_id
        print(AppState.current_user_id)


class DashboardState(AppState):
    """
    the Class used for the dashboard page functions
    events: list[dict] = [] : The list of all events, stored as dictionaries
    selected_event: dict | None = None : the currently selected event represented as a dictionary
    """
    events: list[dict] = []
    selected_event: dict | None = None

    @rx.event
    async def load_events(self):
        """
        Fetches all events from database and converts them into a list of dictionaries
        """
        from eventManagement.services.eventServices import EventServices
        events_list = EventServices.get_all_events()
        self.events = [event.to_dict() for event in events_list]

    # @rx.event
    # async def fetch_and_redirect(self, event_id: int):
    #     from eventManagement.services.eventServices import EventServices
    #     event = EventServices.get_event_by_id(event_id)
    #     if event:
    #         self.selected_event = event.to_dict()
    #         return rx.redirect("/event-detail")
    #     else:
    #         print("ERROR: Event is None when expected not to be.")


class LoginLogic(AppState):
    """
    Class responsible for the logic surrounding Logging-in a user
    form_data : A dictionary that represents the values taken from user-entered inputs
    """
    form_data: dict = {}

    @rx.event
    def handleSubmit(self, formData: dict):
        """
        Is called once the user presses 'Log-in'.
        The values from the inputs called "user_name" and "pass_word" are taken and passed to UserServices function login_user.
        If both the username and password are correct, the corresponding user instance is returned.
        If a user is returned, the State variables selected_user and current_user_id are set from
        the users details, the user is then redirected to their home page.

        If details are incorrect, user remains at the log-in page.
        """
        username = formData.get("user_name")
        password = formData.get("pass_word")
        print(username + " " + password)
        logged_in_user = UserServices.login_user(username, password)
        if (logged_in_user):
            self.reset()
            self.selected_user = logged_in_user
            self.current_user_id = logged_in_user.id
            print(AppState.current_user_id)
            yield rx.redirect("/home")
        print(AppState.current_user_id)


class CreateAccount(AppState):
    """
    Class responsible for the logic surrounding Creating an account
    form_data : A dictionary that represents the values taken from user-entered inputs
    """
    form_data: dict = {}

    @rx.event
    def handleSubmit(self, formData: dict):
        """
        Is called once "Create Account" is clicked
        Once clicked, the value of all user-input fields are passed to UserServices.make_base_user()
        If passed username does not exist in the database, the Create Account details are valid and a new user is created.
        The created user is then returned and the State Variables current_user_id and selected_user are set
        from the user details. The user is then re-directed to their home page.

        If details are bad, or already exist in database, user remains at the Create Account page
        """
        username = formData.get("user_name")
        password = formData.get("pass_word")
        name = formData.get("first_name") + " " + formData.get("last_name")
        email = formData.get("email_address")
        birth = formData.get("date_of_birth")
        phone = formData.get("phone_number")
        correctDetails = UserServices.make_base_user(name, email, birth, password, username, phone)
        print(correctDetails)
        if (correctDetails):
            print("good made user")
            print(correctDetails)
            self.reset()
            self.current_user_id = correctDetails.id
            self.selected_user = correctDetails.to_dict()
            yield rx.redirect("/home")


def index() -> rx.Component:
    """
    UI component for login/ create account page
    """
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
                spacing="5",
                justify="center",
                min_height="85vh",
            ),

        ),
        background="center/cover url('/bg.png')",
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


@rx.page(on_load=DashboardState.load_events)
def dashboard():
    """
    UI component page for dashboard. On load, all events are fetched and loaded.
    The page uses the DashboardState class, to use functions and variables that are relevant to the dashboard
    The UI represents each existing event in a card, with the card details representing the event details
    """
    DashboardState.load_events()

    return rx.container(
        home_header(),
        rx.heading("Events", size="8", padding_top="20px", padding_bottom="20px"),
        rx.container(
            rx.grid(
                rx.foreach(
                    DashboardState.events,
                    lambda event: rx.card(
                        rx.vstack(
                            rx.text(f"{event['name']} {event['event_type']}", font_weight="bold"),
                            rx.text(event["location"], font_style="italic"),
                            rx.text(event["age_range"]),
                        ),
                        height="25vh",
                        on_click=lambda e=event: EventInnards.fetch_and_redirect_for_book(event["id"])
                    )
                ),
                columns="3",
                spacing="4",
                width="100%",
            ),
        ),
    )


class EventInnards(DashboardState):
    """
    EventInnards is the class that re-routes the user, and fetches details pertaining to an event, like event details, perks and registrations.
    perks: list[dict] = A list of the events perks, each represented as a dictionary
    attenders: list[dict] = A list of the events attenders, each represented as a dictionary
    regos: list[dict] = A list of registrations for the event, each represented as a dictionary
    approved_regos: list[dict] =  A list of approved registrations for the event
    rejected_regos: list[dict] = A list of rejected registrations for the event
    user_regos: list[dict] = A list of all registrations of current logged in user
    event_id: int = The id of the currently viewed event
    """
    perks: list[dict] = []
    attenders: list[dict] = []
    regos: list[dict] = []
    approved_regos: list[dict] = []
    rejected_regos: list[dict] = []
    user_regos: list[dict] = []
    event_id: int

    @rx.event
    async def cancel_ticket(self, event_id: int):
        """
        Called when the user clicks cancel event.
        The registration to be deleted is found using the event id and the user id, and then removed from the database
        The user is then redirected to their home page, which shows their existing registrations
        """
        user_registration = UserServices.get_user_registrations_for_event(self.current_user_id, event_id)
        EventServices.remove_registration(user_registration)
        return rx.redirect("/home")

    @rx.event
    async def approve_registration(self, rego_id: int, event_id: int):
        """
        Called when an organiser approves a registration
        The registration to-be-approved is found and returned via the registration id
        The approved boolean of the found registration is set to True
        The list of approved and rejected registrations is then re-fetched and set to reflect the new changes
        """
        EventServices.approve_registration(rego_id)

        regos_temp_app = EventServices.get_all_APPROVED_registrations_on_event(event_id)
        self.approved_regos = UserServices.registration_representer(regos_temp_app)

        regos_temp_rej = EventServices.get_all_REJECTED_registrations_on_event(event_id)
        self.rejected_regos = UserServices.registration_representer(regos_temp_rej)

    @rx.event
    async def reject_registration(self, rego_id: int, event_id: int):
        """
        Called when an organiser rejects a registration
        The registration to-be-rejected is found and returned via the registration id
        The approved boolean of the found registration is set to False
        The list of approved and rejected registrations is then re-fetched and set to reflect the new changes
        """
        EventServices.reject_registration(rego_id)

        regos_temp_app = EventServices.get_all_APPROVED_registrations_on_event(event_id)
        self.approved_regos = UserServices.registration_representer(regos_temp_app)

        regos_temp_rej = EventServices.get_all_REJECTED_registrations_on_event(event_id)
        self.rejected_regos = UserServices.registration_representer(regos_temp_rej)

    @rx.event
    async def fetch_and_redirect(self, event_id: int):
        """
        Called when a user clicks on an event in the users registered events page
        On-click, the user is redirected to a new page which shows the details of their booked event
        The event id of the clicked registration is passed and used to find the event object and its perks, which are shown on the next page
        """
        from eventManagement.services.eventServices import EventServices
        event = EventServices.get_event_by_id(event_id)
        if event:
            self.selected_event = event.to_dict()
            perks_temp = EventServices.get_event_perks_from_event_id(event_id)
            self.perks = [perk.to_dict() for perk in perks_temp]

            user_regs = UserServices.get_user_registrations(self.current_user_id)
            self.user_regos = [rego.to_dict() for rego in user_regs]
            return rx.redirect("/event-detail")
        else:
            print("ERROR: Event is None when expected not to be.")

    @rx.event
    async def fetch_and_redirect_for_book(self, event_id: int):
        """
        Called when the user clicks on an event in the browse event dashboard.
        On-click, the event id is passed and used to set to find the event object and set it as selected_event
        With the selected_event object, the events perks can be found and displayed along with the event details
        """
        from eventManagement.services.eventServices import EventServices
        event = EventServices.get_event_by_id(event_id)
        if event:
            self.selected_event = event.to_dict()
            perks_temp = EventServices.get_event_perks_from_event_id(event_id)
            self.perks = [perk.to_dict() for perk in perks_temp]
            return rx.redirect("/book-ticket")
        else:
            print("ERROR: Event is None when expected not to be.")

    @rx.event
    async def fetch_and_redirect_organised_event(self, event_id: int):
        """
        Called when a user clicks on one of their organised events in the organiser portal
        On-click, the event id is passed and used to set to find the event object and set it as selected_event
        From the event object, the event perks, approved registrations and rejected registrations can be found and displayed
        """
        from eventManagement.services.eventServices import EventServices
        event = EventServices.get_event_by_id(event_id)
        if event:
            self.selected_event = event.to_dict()
            perks_temp = EventServices.get_event_perks_from_event_id(event_id)
            self.perks = [perk.to_dict() for perk in perks_temp]
            attenders_temp = UserServices.get_attenders(event_id)
            self.attenders = [user.to_dict() for user in attenders_temp]
            regos_temp = EventServices.get_all_registrations_on_event(event_id)
            self.regos = [registration.to_dict() for registration in regos_temp]
            with rx.session() as session:
                for rego in self.regos:
                    perk = session.exec(Perk.select().where(Perk.id == rego["perk_id"])).first()
                    rego["perk_name"] = perk.name if perk else "Unknown"

            regos_temp_app = EventServices.get_all_APPROVED_registrations_on_event(event_id)
            regos_temp_rej = EventServices.get_all_REJECTED_registrations_on_event(event_id)
            self.approved_regos = UserServices.registration_representer(regos_temp_app)
            self.rejected_regos = UserServices.registration_representer(regos_temp_rej)
            return rx.redirect("/organised-event-detail")
        else:
            print("ERROR: Event is None when expected not to be.")

    @rx.event
    async def fetch_and_redirect_EDIT_organised_event(self, event_id: int):
        """
        Called when user clicks 'edit event' on their organised event.
        On-click, the event id is passed and used to set to find the event object and set it as selected_event
        From the event object, the event perks, approved registrations and rejected registrations can be found and displayed
        """
        from eventManagement.services.eventServices import EventServices
        event = EventServices.get_event_by_id(event_id)
        if event:
            self.selected_event = event.to_dict()
            perks_temp = EventServices.get_event_perks_from_event_id(event_id)
            self.perks = [perk.to_dict() for perk in perks_temp]
            attenders_temp = UserServices.get_attenders(event_id)
            self.attenders = [user.to_dict() for user in attenders_temp]
            regos_temp = EventServices.get_all_registrations_on_event(event_id)
            self.regos = [registration.to_dict() for registration in regos_temp]
            with rx.session() as session:
                for rego in self.regos:
                    perk = session.exec(Perk.select().where(Perk.id == rego["perk_id"])).first()
                    rego["perk_name"] = perk.name if perk else "Unknown"

            regos_temp_app = EventServices.get_all_APPROVED_registrations_on_event(event_id)
            self.approved_regos = [registration.to_dict() for registration in regos_temp_app]

            regos_temp_rej = EventServices.get_all_REJECTED_registrations_on_event(event_id)
            self.rejected_regos = [registration.to_dict() for registration in regos_temp_rej]

            return rx.redirect("/edit-event")
        else:
            print("ERROR: Event is None when expected not to be.")


class TicketBooking(AppState):
    """
    Class used for ticket-booking logic
    """
    perks: list[dict] = []
    event_id: int
    selected_event: dict | None = None

    selected_perks: list[str] = []
    selected_perk: str = ""
    selected_perk_id: int = -1
    subtotal: int = 0
    cardholder_name: str = ""
    cardholder_number: str = ""
    expiry: str = ""
    cvv: str = ""

    @rx.event
    def pay(self, event: dict):
        """
        Called when the user goes to pay. If no perk is selected and not all fields are filled out, the payment will not go through.
        If all details are filled out, the registration will be made and the user will be redirected to their home page, where they can see thier new registration and its approval status
        """
        print(f"PAY PAY PAY {self.selected_perk} {self.subtotal} {event['name']}")
        if (self.selected_perk != "" and self.subtotal != 0 and self.cardholder_name != "" and self.cardholder_number != "" and self.expiry != "" and self.cvv != ""):
            EventServices.make_rego(self.subtotal, event['id'], self.current_user_id, self.selected_perk_id)
            return rx.redirect("/home")

    @rx.event
    def select_perk(self, perk_name: str, perk_price: int, perk_id: int):
        """
        Called when the user selects a perk card. On click, the perk on the clicked card is set as the selected_perk
        The subtotal is also reset based on the perk price
        """
        print(self.selected_perk)
        self.selected_perk = perk_name
        self.subtotal = perk_price
        self.selected_perk_id = perk_id
        print(self.selected_perk)


    # @rx.event
    # def toggle_perk(self, name: str):
    #     if name in self.selected_perks:
    #         self.selected_perks.remove(name)
    #     else:
    #         self.selected_perks.append(name)

    @rx.event
    def load_event_detail_for_book(self, event_id):
        """
        On entering the book-ticket page, the details of the event being booked are fetched, loaded and set so that
        the functions of TicketBooking can access its details
        """
        from eventManagement.services.eventServices import EventServices
        event = EventServices.get_event_by_id(event_id)
        if event:
            self.selected_event = event.to_dict()
            print("is event")
            perks_temp = EventServices.get_event_perks_from_event_id(event_id)
            self.perks = [perk.to_dict() for perk in perks_temp]

    @rx.event
    def book_ticket_for_event(self, event_id):
        """
        Called when the user clicks book-ticket. On-click the selected event is set from the clicked event_id, the user
        is then redirected
        """
        event = EventServices.get_event_by_id(event_id).to_dict()
        selected_event = event
        print(f"book ticket for {event['name']}")
        return rx.redirect("/make-registration")

    @rx.event
    def set_cardholder_name(self, value: str):
        """
        On change of the cardholder name field, the new value of the input is set as the cardholder name
        """
        self.cardholder_name = value

    @rx.event
    def set_cardholder_number(self, value: str):
        """
        On change of the cardholder number field, the new value of the input is set as the cardholder number
        """
        self.cardholder_number = value

    @rx.event
    def set_expiry(self, value: str):
        """
        On change of the card expiry field, the new value of the input is set as the card expiry date
        """
        self.expiry = value

    @rx.event
    def set_cvv(self, value: str):
        """
        On change of the card cvv field, the new value of the input is set as the cvv
        """
        self.cvv = value


@rx.page(route="/book-ticket", on_load=TicketBooking.load_event_detail_for_book(EventInnards.selected_event['id']))
def book_ticket():
    """
    The Book Ticket page. This page, on load, fetches the details of the event being booked.
    This page shows the details of the event, like its name, date and perks.
    If the user clicks the Book Ticket button, they are redirected to the Make Registration page
    """
    event = EventInnards.selected_event
    return rx.container(
        rx.card(
            rx.vstack(
                rx.heading(event["name"], size="4"),
                rx.text(f"Type: {event['event_type']}"),
                rx.text(f"Location: {event['location']}"),
                rx.text(f"Date: {event['date']}"),
                rx.text(f"Age Range: {event['age_range']}"),
                spacing="3",
                align="start"
            ),
            padding="6",
            shadow="md",
            border_radius="3xl",
            margin_bottom="6",
        ),

        rx.heading("Perks", size="4", margin_bottom="2"),
        rx.grid(
            rx.foreach(
                EventInnards.perks,
                lambda perk: rx.card(
                    rx.vstack(
                        rx.text(perk["name"], font_weight="bold"),
                        rx.text(f"Price: ${perk['price']}"),
                        rx.text(f"Description: {perk['description']}"),
                        rx.text(f"Age Range: {perk['age_range']}"),
                        rx.text(f"Duration: {perk['duration']}"),
                        rx.text(f"Available Slots: {perk['available_slots']}"),
                        spacing="2",
                        align="start"
                    ),
                    padding="4",
                    shadow="sm",
                    border_radius="xl",
                )
            ),
            columns="2",
            spacing="4",
            width="100%",
            margin_bottom="6",
        ),
        rx.button(
            "Book Ticket",
            on_click=TicketBooking.book_ticket_for_event(event["id"]),
            color_scheme="blue",
            size="4"
        ),

        padding="6",
        spacing="6"
    )


@rx.page(route="/make-registration")
def make_registration():
    """
    The UI for the page where the user can make their registration for an event.
    The user can select their perk and fill in their card-information to make a registration
    """
    event = EventInnards.selected_event
    return rx.container(
        rx.heading("Make Registration", size="6", margin_bottom="4"),

        rx.card(
            rx.vstack(
                rx.heading(event['name'], size="4"),
                rx.text(event['event_type']),
                rx.text(event['location']),
                rx.text(event['date']),
                rx.text(event['age_range']),
                spacing="3",
                align="start"
            ),
            padding="6",
            shadow="md",
            border_radius="3xl",
            margin_bottom="6",
        ),

        rx.card(
            rx.vstack(
                rx.heading("Available Perks", size="4", margin_bottom="2"),
                rx.grid(
                    rx.foreach(
                        EventInnards.perks,
                        lambda perk: rx.card(
                            rx.vstack(
                                rx.text(f"{perk['name']} : {perk['price']}", font_weight="bold"),
                                rx.text(perk['description']),
                                spacing="1",
                                align="start"
                            ),
                            padding="3",
                            border_radius="xl",
                            shadow="xs"
                        )
                    ),
                    columns="3",
                    spacing="3",
                    width="100%",
                )
            ),
            padding="4",
            shadow="sm",
            border_radius="xl",
            margin_bottom="6"
        ),

        rx.card(
            rx.vstack(
                rx.heading("Register and Pay", size="4"),
                rx.input(
                    placeholder="Cardholder Name",
                    width="100%",
                    on_change=TicketBooking.set_cardholder_name,
                ),

                rx.input(
                    placeholder="Card Number",
                    type_="number",
                    width="100%",
                    type="number",
                    on_change=TicketBooking.set_cardholder_number,
                ),

                rx.input(
                    placeholder="Expiry Date (MM/YY)",
                    width="100%",
                    on_change=TicketBooking.set_expiry,
                ),

                rx.input(
                    placeholder="CVV",
                    type_="password",
                    width="100%",
                    on_change=TicketBooking.set_cvv,
                ),

                rx.text("Select Perks"),
                rx.foreach(
                    EventInnards.perks,
                    lambda perk: rx.card(
                        rx.vstack(
                            rx.text(f"{perk['name']} : {perk['price']}", font_weight="bold"),
                            rx.text(perk['description']),
                            spacing="1",
                            align="start",
                            on_click=lambda p=perk: TicketBooking.select_perk(p["name"], p["price"], p["id"]),

                        ),
                        padding="3",
                        border_radius="xl",
                        shadow="xs",
                        cursor="pointer",
                        border=rx.cond(
                            TicketBooking.selected_perk == perk["name"],
                            "1px solid #3182ce",
                            "1px solid #e2e8f0"
                        ),
                    )
                ),

                rx.text(f"Subtotal: {TicketBooking.subtotal}", font_weight="bold"),

                rx.button(
                    "Pay",
                    color_scheme="blue",
                    size="4",
                    on_click=TicketBooking.pay(event)
                ),

                spacing="4",
                align="stretch",
                width="100%"
            ),
            padding="6",
            shadow="md",
            border_radius="2xl",
            width="100%"
        ),

        padding="6",
        spacing="6"
    )


# @rx.page(route="/booked-event-detail")
# def booked_event_detail():
#     """
#     The UI page showing the details of the users registered event.
#     """
#     event = EventInnards.selected_event
#     return rx.container(
#         rx.card(
#             rx.vstack(
#                 rx.heading(event["name"], size="4"),
#                 rx.text(f"Type: {event['event_type']}"),
#                 rx.text(f"Location: {event['location']}"),
#                 rx.text(f"Date: {event['date']}"),
#                 rx.text(f"Age Range: {event['age_range']}"),
#                 spacing="3",
#                 align="start"
#             ),
#             padding="6",
#             shadow="md",
#             border_radius="3xl",
#             margin_bottom="6",
#         ),
#
#         rx.heading("Perks", size="4", margin_bottom="2"),
#         rx.grid(
#             rx.foreach(
#                 EventInnards.perks,
#                 lambda perk: rx.card(
#                     rx.vstack(
#                         rx.text(perk["name"], font_weight="bold"),
#                         rx.text(f"Price: ${perk['price']}"),
#                         rx.text(f"Description: {perk['description']}"),
#                         rx.text(f"Age Range: {perk['age_range']}"),
#                         rx.text(f"Duration: {perk['duration']}"),
#                         rx.text(f"Available Slots: {perk['available_slots']}"),
#                         spacing="2",
#                         align="start"
#                     ),
#                     padding="4",
#                     shadow="sm",
#                     border_radius="xl",
#                 )
#             ),
#             columns="2",
#             spacing="4",
#             width="100%",
#             margin_bottom="6",
#         ),
#         # rx.button(
#             # "Cancel Ticket",
#             # color_scheme="green",
#             # size="4"
#         # ),
#
#         padding="6",
#         spacing="6"
#     )


@rx.page(route="/event-detail")
def event_detail():
    """
    The UI for when the user clicks on their registration for an event.
    Here the user can also cancel their registration by clicking the Cancel Ticket button
    """
    event = EventInnards.selected_event
    return rx.container(
        rx.card(
            rx.vstack(
                rx.heading(event["name"], size="4"),
                rx.text(f"Type: {event['event_type']}"),
                rx.text(f"Location: {event['location']}"),
                rx.text(f"Date: {event['date']}"),
                rx.text(f"Age Range: {event['age_range']}"),
                spacing="3",
                align="start"
            ),
            padding="6",
            shadow="md",
            border_radius="3xl",
            margin_bottom="6",
        ),

        rx.heading("Perks", size="4", margin_bottom="2"),
        rx.grid(
            rx.foreach(
                EventInnards.perks,
                lambda perk: rx.card(
                    rx.vstack(
                        rx.text(perk["name"], font_weight="bold"),
                        rx.text(f"Price: ${perk['price']}"),
                        rx.text(f"Description: {perk['description']}"),
                        rx.text(f"Age Range: {perk['age_range']}"),
                        rx.text(f"Duration: {perk['duration']}"),
                        rx.text(f"Available Slots: {perk['available_slots']}"),
                        spacing="2",
                        align="start"
                    ),
                    padding="4",
                    shadow="sm",
                    border_radius="xl",
                )
            ),
            columns="2",
            spacing="4",
            width="100%",
            margin_bottom="6",
        ),
        rx.button(
            "Cancel Ticket",
            on_click=lambda e=event: EventInnards.cancel_ticket(event["id"]),
            color_scheme="red",
            size="4"
        ),

        padding="6",
        spacing="6"
    )

@rx.page(route="/organised-event-detail")
def event_detail():
    """
    The UI for when a user clicks on an event in their organiser portal. This page shows the details of the event.
    This page also allows the organiser to see all the registrations and approve / reject each registration.
    If the user clicks the 'edit event' page, they will be redirected to  a page where they can edit the event and its perks
    """
    event = EventInnards.selected_event
    print(event['id'])
    return rx.container(
        rx.vstack(
            home_header(),
            rx.card(
                rx.vstack(
                    rx.heading(event["name"], size="7"),
                    rx.text(f"Type: {event['event_type']}"),
                    rx.text(f"Location: {event['location']}"),
                    rx.text(f"Date: {event['date']}"),
                    rx.text(f"Age Range: {event['age_range']}"),
                    spacing="3",
                    align="start"
                ),
                padding="6",
                shadow="md",
                border_radius="3xl",
                margin_bottom="6",
            ),

            rx.heading("Perks", size="6", margin_bottom="2"),
            rx.grid(
                rx.foreach(
                    EventInnards.perks,
                    lambda perk: rx.card(
                        rx.vstack(
                            rx.text(perk["name"], font_weight="bold"),
                            rx.text(f"Price: ${perk['price']}"),
                            rx.text(f"Description: {perk['description']}"),
                            rx.text(f"Age Range: {perk['age_range']}"),
                            rx.text(f"Duration: {perk['duration']}"),
                            rx.text(f"Available Slots: {perk['available_slots']}"),
                            spacing="2",
                            align="start"
                        ),
                        padding="4",
                        shadow="sm",
                        border_radius="xl",
                    )
                ),
                columns="2",
                spacing="4",
                width="100%",
                margin_bottom="6",
            ),
            # rx.button(
            #     "Book Event",
            #     # on_click=DashboardState.book_selected_event,
            #     color_scheme="green",
            #     size="4"
            # ),
            columns="2",
            spacing="4",
            width="100%",
            margin_bottom="6",
        ),
        rx.heading("Registrations", size="4", margin_bottom="2"),
        rx.grid(
            rx.vstack(
                rx.heading("Rejected", size="3"),
                rx.foreach(
                    EventInnards.rejected_regos,
                    lambda rego: rx.card(
                        rx.vstack(
                            rx.text(f"Registration ID: {rego['id']}"),
                            rx.text(f"Perk: {rego['perk_name']}"),
                            rx.text(f"Approved: {rego['approved']}"),

                            rx.button(
                                "Approve",
                                on_click=lambda r=rego: EventInnards.approve_registration(r["id"], event["id"]),
                                size="2",
                                color_scheme="green"
                            )
                        ),
                        padding="3",
                        border_radius="xl",
                        shadow="xs",
                        width="100%"
                    )
                ),
                spacing="2"
            ),
            rx.vstack(
                rx.heading("Approved", size="3"),
                rx.foreach(
                    EventInnards.approved_regos,
                    lambda rego: rx.card(
                        rx.vstack(
                            rx.text(f"Registration ID: {rego['id']}"),
                            rx.text(f"Perk: {rego['perk_name']}"),
                            rx.text(f"Approved: {rego['approved']}"),
                            rx.button(
                                "Reject",
                                on_click=lambda r=rego: EventInnards.reject_registration(r["id"], event["id"]),
                                size="2",
                                color_scheme="red"
                            )
                        ),
                        padding="3",
                        border_radius="xl",
                        shadow="xs",
                        width="100%"
                    )
                ),
                spacing="2"
            ),
            columns="2",
            spacing="6",
            width="100%",
        ),
        # rx.button(
        #     "Edit Event",
        #     on_click=EventInnards.fetch_and_redirect_EDIT_organised_event(event["id"]),
        #     color_scheme="blue",
        #     size="4"
        # ),

            padding="5",
            spacing="5",
        ),



class OrganiserPortal(AppState):
    """
    The class that holds the functions and variables for the Organiser Portal
    organised_events: list[dict] = The list of dictionary representations of users organised events
    """
    organised_events: list[dict] = []

    @rx.event
    async def organiser_portal_on_load(self):
        """
        Called On load, the organised events of the user are fetched and set
        """
        from eventManagement.services.user_services import UserServices
        organiser = UserServices.get_organiser_from_base_user(self.current_user_id)
        if organiser:
            events = UserServices.get_organised_events(organiser.id)
            self.organised_events = [event.to_dict() for event in events]


@rx.page(route="/organiser_portal", on_load=OrganiserPortal.organiser_portal_on_load)
def user_home_page():
    """
    The Organiser Portal UI. Here the user can see cards for each of their organised events
    """
    AppState.fetch_current_user()
    return rx.container(
        home_header(),
        rx.card(
            rx.vstack(
                rx.heading(f"Welcome {AppState.selected_user['name']}!"),
                rx.text(f"Email: {AppState.selected_user['email']}"),
                rx.text(f"Username: {AppState.selected_user['username']}"),
                rx.text(f"Phone number: {AppState.selected_user['phone_number']}"),
                align="start",
                spacing="2",
            ),
            shadow="md",
            padding="4",
            border_radius="5xl",
        ),

        rx.cond(
            OrganiserPortal.organised_events,
            rx.vstack(
                rx.heading("Your Organised Events", size="4", padding_bottom="2"),
                rx.grid(
                    rx.foreach(
                        OrganiserPortal.organised_events,
                        lambda event: rx.card(
                            rx.vstack(
                                rx.text(event["name"], font_weight="bold"),
                                rx.text(event["event_type"]),
                                rx.text(event["location"]),
                                rx.text(event["date"]),
                            ),
                            height="25vh",
                            on_click=lambda e=event: EventInnards.fetch_and_redirect_organised_event(event["id"])
                        )
                    ),
                    columns="2",
                    spacing="4",
                    width="100%",
                ),
                align="start",
                spacing="4",
                padding_top="4",
            ),
            rx.text("No organised events.")
        ),

        rx.button(
            "Create New Event",
            on_click=rx.redirect("/create-event"),
            color_scheme="blue",
            size="3",
            margin_top="4"
        )
    )

class EditEvent(AppState):
    """
    The Class for editing an event and its perks
    perks: list[dict] = a list of the events perks, in dictionary form
    event_type: dict = the events type
    edit_perks_popover: bool = False = When edit perk is clicked, it is set to true and the edit-perk popover appears
    event_created: bool = False = If no event has been created, the create perk button will not appear
    form_data: dict = {} = The value of the input forms
    event_id: int = -1 = The current event id
    organised_events: list[dict] = [] = The users organised events

    """
    perks: list[dict] = []
    event_type: dict
    edit_perks_popover: bool = False
    event_created: bool = False
    form_data: dict = {}
    event_id: int = -1
    organised_events: list[dict] = []

    def mark_created(self):
        """
        If an event has been made and submitted, boolean is set to true, allowing the user to edit perks
        """
        self.event_created = True

    @rx.event
    async def on_load_for_edit(self):
        """
        On Load, the users organised events are loaded. If the user has never made an event, an Organiser is made using their user id
        The Perks of the current event are also loaded
        """
        self.event_type = {e.value: e.value.capitalize() for e in EventType}
        self.event_created = False;
        from eventManagement.services.user_services import UserServices
        organiser = UserServices.get_organiser_from_base_user(self.current_user_id)
        if (organiser == None):
            UserServices.make_organiser(self.current_user_id)
        else:
            events = UserServices.get_organised_events(organiser.id)
            self.organised_events = [event.to_dict() for event in events]

        from eventManagement.services.eventServices import EventServices
        perks_temp = EventServices.get_event_perks_from_event_id(self.event_id)
        self.perks = [perk.to_dict() for perk in perks_temp]

    @rx.event
    async def load_perks(self):
        """
        Loads the perks for the current event, and converts them to a list of dictionaries
        """
        from eventManagement.services.eventServices import EventServices
        perks_temp = EventServices.get_event_perks_from_event_id(self.event_id)
        if perks_temp:
            self.perks = [perk.to_dict() for perk in perks_temp]
        else:
            self.perks = []

    @rx.event
    async def make_event(self, formData: dict):
        """
        On submit, the values of the input forms are taken and passed to EventServices.make_event()
        """
        date_str = formData.get("date")
        date_str = formData.get("date")
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        print(date_str)
        print(date_obj)
        name = formData.get("name")
        duration = formData.get("duration")
        date = date_obj
        location = formData.get("location")
        desc = formData.get("description")
        low_age = formData.get("low_age")
        high_age = formData.get("high_age")
        capacity = formData.get("capacity")
        event_type = formData.get("type")
        event_status = formData.get("status")
        age_range = str(low_age) + " to " + str(high_age)
        from eventManagement.services.eventServices import EventServices
        new_event_made = EventServices.create_event(name, duration, event_type, date, location, 0, 0, desc, age_range,
                                                   event_status,
                                                   capacity, self.current_user_id)

        self.event_id = new_event_made.get("id")
        await self.load_perks()

    # TO BE IMPLEMENTED
    @rx.event
    async def make_new_perk(self):
        print("make new perk")

    # TO BE IMPLEMENTED
    @rx.event
    async def edit_perk(self):
        print("edit perk")

    @rx.event
    async def handleSubmitOnNewPerk(self, formData: dict):
        username = formData.get("perk_name")
        password = formData.get("perk_price")
        print(username + " " + password)
        from eventManagement.services.eventServices import EventServices
        EventServices.set_perk(formData.get("perk_name"), formData.get("perk_duration"), formData.get("perk_price"),
                               formData.get("perk_description"),
                               str(formData.get("perk_age_range_highest")) + " to" + str(
                                   formData.get("perk_age_range_lowest")), formData.get("perk_slots"), self.event_id, )

        await self.load_perks()


def editPerkPopover():
    return rx.dialog.content(
        rx.dialog.title("New Perk"),
        rx.container(
            rx.vstack(
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="Name",
                            name="perk_name",
                            width="100%"

                        ),
                        rx.input(
                            placeholder="Price",
                            name="perk_price",
                            type="number",
                            width="100%"

                        ),
                        rx.input(
                            placeholder="Description",
                            name="perk_description",
                            width="100%"

                        ),
                        rx.input(
                            placeholder="Age Range Lowest",
                            name="perk_age_range_lowest",
                            type="number",
                            width="100%"

                        ),
                        rx.input(
                            placeholder="Age Range Highest",
                            name="perk_age_range_highest",
                            type="number",
                            width="100%"

                        ),
                        rx.input(
                            placeholder="Duration",
                            name="perk_duration",
                            type="number",
                            width="100%"

                        ),
                        rx.input(
                            placeholder="Available Slots",
                            name="perk_slots",
                            type="number",
                            width="100%"
                        ),
                        rx.button("Submit", type="submit"),
                        align="center",
                    ),
                    rx.grid(
                        rx.foreach(
                            EditEvent.perks,
                            lambda perk: rx.card(
                                rx.vstack(
                                    rx.heading(perk["name"]),
                                    rx.text(f"Price : {perk['price']}"),
                                    rx.text(f"Description : {perk['description']}"),
                                    rx.text(f"Age Range : {perk['age_range']}"),
                                    rx.text(f"Duration : {perk['duration']} hour"),
                                    rx.text(f"Available Slots : {perk['available_slots']}"),
                                    rx.button("Delete"),
                                    rx.button("Edit"),
                                )
                            )
                        ),
                        columns="3",
                        spacing="4",
                    ),
                ),
            ),
        ),
        rx.dialog.close(
            rx.button("Close", size="3"),
        ),
    ),


@rx.page(route="/edit-event", on_load=EditEvent.on_load_for_edit())
def edit_event():
    """
    The Ui for the edit event page, where the user can edit the event and its perks
    """
    event = EventInnards.selected_event
    return rx.center(
        rx.vstack(
            rx.heading("Edit Event!"),
            rx.card(
                rx.form(
                    rx.vstack(
                        rx.input(placeholder="name", name="name", width="100%", value=event['name']),
                        rx.input(placeholder="Event Duration", name="duration", type="number", width="100%",
                                 value=event['duration']),
                        rx.select(
                            [e.value for e in EventType.list()],
                            name="type"
                            , width="100%", value=event['event_type']),
                        rx.input(placeholder="Event Date", name="date", type="date", width="100%", value=event['date']),
                        rx.input(placeholder="Event Location", name="location", width="100%", value=event['location']),
                        rx.input(placeholder="Event Description", name="description", width="100%",
                                 value=event['description']),
                        rx.input(placeholder="Age Range Lowest", type="number", name="low_age", width="100%"),
                        rx.input(placeholder="Age Range Highest", type="number", name="high_age", width="100%"),
                        rx.select(
                            [e.value for e in EventStatus.list()],
                            name="status"
                            , width="100%", value=event['status']),
                        rx.input(placeholder="Capacity", type="number", name="capacity", width="100%",
                                 value=event['capacity']),
                        rx.button("Submit Event", type_="submit"),
                    ),
                    on_submit=EditEvent.make_event
                ),

                width="100%"
            ),
            rx.grid(
                rx.foreach(
                    EditEvent.perks,
                    lambda perk: rx.card(
                        rx.vstack(
                            rx.heading(perk["name"]),
                            rx.text(f"Price : {perk['price']}"),
                            rx.text(f"Description : {perk['description']}"),
                            rx.text(f"Age Range : {perk['age_range']}"),
                            rx.text(f"Duration : {perk['duration']} hour"),
                            rx.text(f"Available Slots : {perk['available_slots']}"),
                            rx.button("Delete"),
                            rx.button("Edit"),
                        )
                    )
                ),
                columns="3",
                spacing="4",
            ),
            width="80%"
        )
    )


class CreateEvent(AppState):
    """
    The Class for creating an event, and its perks

    perks: list[dict] = a list of the events perks, in dictionary form
    event_type: dict = the events type
    edit_perks_popover: bool = False = When edit perk is clicked, it is set to true and the edit-perk popover appears
    event_created: bool = False = If no event has been created, the create perk button will not appear
    form_data: dict = {} = The value of the input forms
    event_id: int = -1 = The current event id
    organised_events: list[dict] = [] = The users organised events
    """
    perks: list[dict] = []
    event_type: dict
    edit_perks_popover: bool = False
    event_created: bool = False
    form_data: dict = {}
    event_id: int = -1
    organised_events: list[dict] = []

    def mark_created(self):
        """
        If an event has been created, the boolean is set to true, revealing the 'make perk' button
        """
        self.event_created = True

    @rx.event
    async def create_event_on_load(self):
        """
        Called on load of the create-event page. If the user has never created an event, a new Organiser is made using their id
        If the user has made events / is an Organiser, their organised events are shown
        """
        self.event_type = {e.value: e.value.capitalize() for e in EventType}
        if self.event_id > 0:
            await self.load_perks()
        self.event_created = False;
        from eventManagement.services.user_services import UserServices
        organiser = UserServices.get_organiser_from_base_user(self.current_user_id)

        if (organiser == None):
            UserServices.make_organiser(self.current_user_id)
        else:
            events = UserServices.get_organised_events(organiser.id)
            self.organised_events = [event.to_dict() for event in events]

    @rx.event
    async def load_perks(self):
        """
        Loads the perks of the current event using the event id
        """
        from eventManagement.services.eventServices import EventServices
        perks_temp = EventServices.get_event_perks_from_event_id(self.event_id)
        if perks_temp:
            self.perks = [perk.to_dict() for perk in perks_temp]
        else:
            self.perks = []

    @rx.event
    async def make_event(self, formData: dict):
        """
        Called when the user clicks 'submit' in the event creation page.
        The value of the inputs forms is taken and used to make an event using EventServices.create_event
        Once made, the event_created boolean is set to True, revealing the 'make perk' button to the user
        """
        date_str = formData.get("date")
        date_str = formData.get("date")
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        print(date_str)
        print(date_obj)
        name = formData.get("name")
        duration = formData.get("duration")
        date = date_obj
        location = formData.get("location")
        desc = formData.get("description")
        low_age = formData.get("low_age")
        high_age = formData.get("high_age")
        capacity = formData.get("capacity")
        event_type = formData.get("type")
        event_status = formData.get("status")
        age_range = str(low_age) + " to " + str(high_age)
        from eventManagement.services.eventServices import EventServices
        newly_created_event = EventServices.create_event(name, duration, event_type, date, location, 0, 0, desc, age_range,
                                                   event_status,
                                                   capacity, self.current_user_id)

        self.event_created = True
        self.event_id = newly_created_event.get("id")
        self.event_created = True

        await self.load_perks()

    @rx.event
    async def make_new_perk(self):
        print("make new perk")

    @rx.event
    async def edit_perk(self):
        print("edit perk")

    @rx.event
    async def handleSubmitOnNewPerk(self, formData: dict):
        """
        Called when 'submit' is called on the create perk popover
        The value of the input forms is taken and passed to EventServices.set_perk
        Once a perk is made, the events perks are reloaded, to reflect the newly made perk in the ui
        """
        username = formData.get("perk_name")
        password = formData.get("perk_price")
        print(username + " " + password)
        from eventManagement.services.eventServices import EventServices
        EventServices.set_perk(formData.get("perk_name"), formData.get("perk_duration"), formData.get("perk_price"),
                               formData.get("perk_description"),
                               str(formData.get("perk_age_range_highest")) + " to" + str(
                                   formData.get("perk_age_range_lowest")), formData.get("perk_slots"), self.event_id, )

        await self.load_perks()


def perkPopover():
    """
    The creat perk popover that appears when the user clicks the 'make perk' button
    """
    return rx.dialog.content(
        rx.dialog.title("New Perk"),
        rx.container(
            rx.vstack(
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="Name",
                            name="perk_name",
                            width="100%"
                        ),
                        rx.input(
                            placeholder="Price",
                            name="perk_price",
                            type="number",
                            width="100%"

                        ),
                        rx.input(
                            placeholder="Description",
                            name="perk_description",
                            width="100%"

                        ),
                        rx.input(
                            placeholder="Age Range Lowest",
                            name="perk_age_range_lowest",
                            type="number",
                            width="100%"

                        ),
                        rx.input(
                            placeholder="Age Range Highest",
                            name="perk_age_range_highest",
                            type="number",
                            width="100%"

                        ),
                        rx.input(
                            placeholder="Duration",
                            name="perk_duration",
                            type="number",
                            width="100%"

                        ),
                        rx.input(
                            placeholder="Available Slots",
                            name="perk_slots",
                            type="number",
                            width="100%"
                        ),
                        rx.button("Submit", type="submit"),
                        align="center",
                    ),
                    on_submit=CreateEvent.handleSubmitOnNewPerk,
                    reset_on_submit=True,
                ),
            ),
        ),
        rx.dialog.close(
            rx.button("Close", size="3"),
        ),
    ),


@rx.page(route="/create-event", on_load=CreateEvent.create_event_on_load())
def create_event():
    """
    The UI for creating an event. Here the user can make an event and its perks.
    """
    return rx.center(
        rx.vstack(
            rx.heading("Create New Event!"),
            rx.card(
                rx.form(
                    rx.vstack(
                        rx.input(placeholder="Event Name", name="name", width="100%"),
                        rx.input(placeholder="Event Duration", name="duration", type="number", width="100%"),
                        rx.select(
                            [e.value for e in EventType.list()],
                            name="type"
                            , width="100%"),
                        rx.input(placeholder="Event Date", name="date", type="date", width="100%"),
                        rx.input(placeholder="Event Location", name="location", width="100%"),
                        rx.input(placeholder="Event Description", name="description", width="100%"),
                        rx.input(placeholder="Age Range Lowest", type="number", name="low_age", width="100%"),
                        rx.input(placeholder="Age Range Highest", type="number", name="high_age", width="100%"),
                        rx.select(
                            [e.value for e in EventStatus.list()],
                            name="status"
                            , width="100%"),
                        rx.input(placeholder="Capacity", type="number", name="capacity", width="100%"),
                        rx.button("Submit Event", type_="submit"),
                    ),
                    on_submit=CreateEvent.make_event
                ),

                width="100%"
            ),
            rx.cond(
                CreateEvent.event_created,
                rx.dialog.root(
                    rx.dialog.trigger(rx.button("Create New Perk", size="3")),
                    perkPopover()
                )
            ),
            rx.grid(
                rx.foreach(
                    CreateEvent.perks,
                    lambda perk: rx.card(
                        rx.vstack(
                            rx.heading(perk["name"]),
                            rx.text(f"Price : {perk["price"]}"),
                            rx.text(f"Description : {perk["description"]}"),
                            rx.text(f"Age Range : {perk["age_range"]}"),
                            rx.text(f"Duration : {perk["duration"]} hour"),
                            rx.text(f"Available Slots : {perk["available_slots"]}"),

                            rx.button("Delete"),
                            rx.button("Edit"),
                        )
                    )
                ),
                columns="3",
                spacing="4",
            ),
            width="80%"
        )
    )


class UserHomePage(AppState):
    """
    The class in control of the users home page
     attending_events: list[dict] = [] = the users registrations
    """
    attending_events: list[dict] = []

    @rx.event
    async def home_page_on_load(self):
        """
        Called when the user loads into the home page. The users registrations are fetched and set as attending_events
        """
        from eventManagement.services.user_services import UserServices
        events = UserServices.get_user_registrations(self.current_user_id)
        self.attending_events = UserServices.registration_representer(events)


@rx.page(route="/home", on_load=UserHomePage.home_page_on_load)
def user_home_page():
    """
    The UI for the users home page. Here the user can see their registrations, and browse to find new events to attend
    If the user clicks on a registration, they are redirected to a new page where they can view their registration for that event, and cancel their ticket
    """
    AppState.fetch_current_user()
    return rx.container(
        rx.vstack(
            home_header(),
            rx.dialog.root(
                rx.dialog.content(
                    rx.dialog.title(rx.heading(f"Welcome {AppState.selected_user['name']}!"),),
                    rx.dialog.description(
                        rx.vstack(
                            rx.text(f"Email: {AppState.selected_user['email']}"),
                            rx.text(f"Username: {AppState.selected_user['username']}"),
                            rx.text(f"Phone number: {AppState.selected_user['phone_number']}"),
                            align="start",
                            spacing="2",
                        ),
                        shadow="md",
                        padding="20",
                        border_radius="5xl",
                    ),
                    padding="20",
                ),
                default_open=True,
                padding="20px",
            ),
            shadow="md",
            padding="4",
            border_radius="5xl",
        ),

        rx.cond(
            UserHomePage.attending_events,
            rx.vstack(
                rx.heading("Your Registrations", size="4", padding_bottom="2"),
                rx.grid(
                    rx.foreach(
                        UserHomePage.attending_events,
                        lambda event: rx.card(
                            rx.vstack(
                                rx.text(f"{event["event_name"]} {event["event_type"]}", font_weight="bold"),
                                rx.text(f"Perk : {event["perk_name"]}"),
                                rx.text(f"Price : {event["price"]}"),
                                rx.text(f"Event Date : {event["event_date"]}"),
                                rx.text(f"Event Status : {event["event_status"]}"),
                                rx.text(f"Approved : {event["approved"]}"),
                            ),
                            height="30vh",
                            on_click=lambda e=event: EventInnards.fetch_and_redirect(event["event_id"])
                        )
                    ),
                    align="start",
                    spacing="4",
                    padding_top="4",
                ),
                # rx.text("Not attending any events.")
            ),
            rx.button(
                "Browse Events",
                on_click=rx.redirect("/dashboard"),
                color_scheme="blue",
                size="3",
                margin_top="5"
            ),
        ),
    )

def navbar_link(text: str, url: str) -> rx.Component:
    """The UI component for the navigation header"""
    return rx.link(
        rx.text(text, size="4", weight="medium"), href=url
    )


def header() -> rx.Component:
    """
    The ui component for the header
    """
    return rx.box(
        rx.color_mode.button(position="top-right"),
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.link(
                        rx.image(
                            src="/logo.jpg",
                            width="2.25em",
                            height="auto",
                            border_radius="25%",
                        ),
                        href="/home"
                    ),
                    rx.link(rx.heading("Zen Planner", size="7", weight="bold"),href="/home"),
                    align_items="center",
                ),
                rx.hstack(
                    navbar_link("Home", "/home"),
                    navbar_link("About", "/about"),
                    navbar_link("Dashboard", "/dashboard"),
                    navbar_link("Purely Testing", "/testing"),
                    spacing="4",
                    align_items="center",
                    justify="center"
                ),
                login_logic(),
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


organiser_portal_now = False;


def home_header() -> rx.Component:
    return rx.box(
        rx.color_mode.button(position="top-right"),
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.link(
                        rx.image(
                            src="/logo.jpg",
                            width="2.25em",
                            height="auto",
                            border_radius="25%",
                        ),
                        href="/home"
                    ),
                    rx.link(rx.heading("Zen Planner", size="7", weight="bold"),href="/home"),
                    align_items="center",
                ),
                rx.hstack(
                    navbar_link("Home", "/home"),
                    navbar_link("Browse Events", "/dashboard"),
                    navbar_link("My Events", "/organiser_portal"),
                    #navbar_link("Organiser Portal", "/organiser_portal"),
                    spacing="4",
                    align_items="center",
                    justify="center"
                ),
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

app.add_page(index)
app.add_page(dashboard, route="/dashboard")
app.add_page(aboutUs, route="/about")
app.add_page(pureTesting(), route="/testing")

# Moved into separate file
# seed_users()
# disperse_users_into_roles()
# seed_events()
# seed_one_attendee()
# seed_all_attendees()
# seed_all_organisers()
# seed_perks()
# seed_all_registrations()



