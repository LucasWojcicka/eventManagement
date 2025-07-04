from datetime import datetime
import reflex as rx
import sqlalchemy
from sqlalchemy import create_engine
from faker import Faker
import random
from eventManagement.models.user import User
from eventManagement.models.event import Event, EventType, EventStatus, Perk, Registration
from eventManagement.models.attendee import Attendee
from eventManagement.models.organiser import Organiser


def seed_users():
    """
    creates 50 Fake users using Faker() for data.
    """
    fake = Faker()
    print("seed users")
    with rx.session() as session:
        existing_data = session.exec(User.select()).first()
        if existing_data:
            print(f"already data, pass: {existing_data}")
            session.exec(sqlalchemy.text("DELETE FROM User"))
            session.commit()

        session.commit()
        user = User(name="User User",
                    email="user@mail.com",
                    date_of_birth=fake.date_of_birth(),
                    password="user",
                    username="user",
                    phone_number="1234")
        session.add(user)
        print(user)
        session.commit()
        for x in range(49):
            first_name = fake.first_name()
            last_name = fake.last_name()
            test_user = User(name=first_name + " " + last_name,
                             email=fake.email(),
                             date_of_birth=fake.date_of_birth(),
                             password=fake.password(),
                             username=fake.user_name(),
                             phone_number=fake.phone_number())

            session.add(test_user)
            print(test_user)
            session.commit()


def disperse_users_into_roles():
    """
    assigns created users into roles of Attendee, Organiser or both
    """
    print("$*(#^$*(#$^@#*$^@#$(@#^$*@(#^$@#^$*(^%$Y(*@#$^#@$(^")
    print("attendee or organiser")
    print("ratio of : just attendeee, just organiser, or both")
    fake = Faker()
    print("seed users")
    with rx.session() as session:
        session.exec(sqlalchemy.text("DELETE FROM Attendee"))
        session.exec(sqlalchemy.text("DELETE FROM Organiser"))
        session.commit()
        users = session.query(User).all()
        for i, user in enumerate(users):
            print(f"User {i} -> DB ID: {user.id}")

            if i <= 30:
                print("just attendee")
                attendee = Attendee(user_id=user.id)
                session.add(attendee)
            elif i > 30 and i <= 40:
                print("both")
                attendee = Attendee(user_id=user.id)
                organiser = Organiser(user_id=user.id)
                session.add(attendee)
                session.add(organiser)
            else:
                print("just organiser")
                organiser = Organiser(user_id=user.id)
                session.add(organiser)

        session.commit()


def get_random_event_type():
    """
    gets a random event type from EventType enumeration for sample event creation
    """
    print(len(EventType.list()))
    event_type_list = EventType.list()
    max = len(EventType.list())
    random.seed = datetime.time
    random_index = random.randrange(0, max)
    return event_type_list[random_index].value


def get_random_event_status():
    """
    gets a random status type from EventType enumeration for sample event creation
    """
    print(len(EventType.list()))
    event_status_list = EventStatus.list()
    max = len(EventStatus.list())
    random.seed = datetime.time
    random_index = random.randrange(0, max)
    return event_status_list[random_index].value


def fake_convention_venue():
    """
    creates a fake convention venue for sample event creation
    """
    fake = Faker()
    venue_suffixes = ["Convention Center", "Expo Hall", "Event Pavilion", "Auditorium", "Arena", "Dome",
                      "Exhibition Centre", "Convention Ground", "Meeting Ground", "Hall"]
    venue_name = fake.word().title() + " " + random.choice(venue_suffixes)

    street_address = fake.street_address()
    city = fake.city()
    state = fake.state_abbr()
    zip_code = fake.zipcode()

    full_address = f"{venue_name}\n{street_address}\n{city}, {state} {zip_code}"
    return full_address


def seed_events():
    """
    create sample events using Faker() for fake data
    """
    print("events")
    with rx.session() as session:
        session.exec(sqlalchemy.text("DELETE FROM Event"))
        session.exec(sqlalchemy.text("DELETE FROM Perk"))
        session.exec(sqlalchemy.text("DELETE FROM Registration"))
        session.commit()
        fake = Faker()

        for x in range(25):
            random.seed = datetime.time
            seeded_venue = fake_convention_venue()
            seeded_event_type = get_random_event_type()
            seeded_event_status = get_random_event_status()
            price_range_lower = random.randrange(10, 500, 10)
            price_range_higher = random.randrange((price_range_lower + 100), ((price_range_lower + 100) * 2), 10)
            age_range_lower = random.randrange(0, 75, 5)
            age_range_higher = random.randrange(age_range_lower, 75, 5)
            seeded_capacity = random.randrange(100, 30000, 100)
            seeded_duration = random.randrange(1, 6, 1)
            seeded_date = fake.date_this_year(after_today=True)
            seeded_time = fake.time_object()
            make_date = datetime(seeded_date.year, seeded_date.month, seeded_date.day, seeded_time.hour,
                                 seeded_time.minute, seeded_time.second)
            print("*(&#$#$(*&@#$)(O#I@$)(@#$#@$I&)@#")

            new_event = Event(name=str(fake.word().title()),
                              duration=seeded_duration,
                              event_type=seeded_event_type,
                              # event_type="seed",
                              date=make_date,
                              # location=str(fake.address()),
                              location=str(seeded_venue),
                              price_range_lowest=price_range_lower,
                              price_range_highest=price_range_higher,
                              description=fake.paragraph(1),
                              age_range=str(age_range_lower) + " to " + str(age_range_higher),
                              attendees_num=0,
                              # status=seeded_event_status,
                              status=EventStatus.NORMAL.value,
                              capacity=seeded_capacity,
                              occupied_capacity=0
                              )
            session.add(new_event)
        session.commit()


def seed_one_attendee():
    with rx.session() as session:
        one_attendee = session.exec(Attendee.select()).first()
        one_event = session.exec(Event.select()).first()
        one_attendee.events.append(one_event)
        session.commit()



def seed_all_attendees():
    """
    create sample attendees from user pool
    """
    with rx.session() as session:
        session.exec(sqlalchemy.text("DELETE FROM Attendeeeventlink"))
        session.commit()

        all_attendees = session.exec(Attendee.select()).all()
        all_events = session.exec(Event.select()).all()

        for attendee in all_attendees:
            if random.random() < 0.8:
                num_events = random.randint(1, 5)
                events_to_add = random.sample(all_events, k=min(num_events, len(all_events)))

                for event in events_to_add:
                    attendee.events.append(event)

        session.commit()


def seed_all_registrations():
    """
    create sample registrations from Attendee pool
    """
    with rx.session() as session:
        fake = Faker()
        session.exec(sqlalchemy.text("DELETE FROM registration"))
        session.commit()

        all_attendees = session.exec(Attendee.select()).all()
        for attendee in all_attendees:
            for event in attendee.events:
                base_user = session.exec(
                    User.select().where(User.id == attendee.user_id)
                ).first()

                current_event = session.exec(
                    Event.select().where(Event.id == event.id)
                ).first()
                if not current_event:
                    continue

                event_perks = session.exec(
                    Perk.select().where(Perk.event_id == current_event.id)
                ).all()
                if not event_perks:
                    continue

                random_perk = random.choice(event_perks)

                latest_possible = current_event.date
                registration_date = fake.date_time_between(
                    start_date="-1y", end_date=latest_possible
                )

                is_approved = random.choice([True, False])
                approved_date = (
                    fake.date_time_between(
                        start_date=registration_date,
                        end_date=latest_possible
                    ) if is_approved else None
                )

                new_registration = Registration(
                    price=random_perk.price,
                    approved=is_approved,
                    event_id=current_event.id,
                    user_id=base_user.id,
                    perk_id=random_perk.id,
                    registration_date=registration_date,
                    approved_date=approved_date,
                )

                session.add(new_registration)

        session.commit()

def seed_all_organisers():
    """
    create sample organisers from user pool
    """
    import random
    with rx.session() as session:
        session.exec(sqlalchemy.text("DELETE FROM Organisereventlink"))
        session.commit()

        all_organisers = session.exec(Organiser.select()).all()
        all_events = session.exec(Event.select()).all()

        for event in all_events:
            if all_organisers:
                organiser = random.choice(all_organisers)
                organiser.events.append(event)

        session.commit()


def seed_perks():
    """
    create sample perks for sample events
    """
    with rx.session() as session:
        fake = Faker()
        events = session.query(Event).all()
        for i, event in enumerate(events):
            for x in range(1, random.randrange(2, 6, 1)):
                new_perk = Perk(
                    name=str(fake.word().title()) + " Experience",
                    price=random.randrange(10, 200, 10),
                    description=fake.paragraph(1),
                    age_range=event.age_range,
                    duration=random.randrange(1, 5, 1),
                    available_slots=random.randrange(10, 400, 10),
                    event_id=event.id
                )
                session.add(new_perk)
        session.commit()
