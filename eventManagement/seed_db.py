from eventManagement.models.seed_data import (
    seed_users,
    disperse_users_into_roles,
    seed_events,
    seed_one_attendee,
    seed_all_attendees,
    seed_all_organisers,
    seed_perks,
    seed_all_registrations
)

def seed_database():
    """Run all database seeding operations in the correct order"""
    print("Starting database seeding...")
    
    print("Seeding users...")
    seed_users()
    
    print("Dispersing users into roles...")
    disperse_users_into_roles()
    
    print("Seeding events...")
    seed_events()
    
    print("Seeding one attendee...")
    seed_one_attendee()
    
    print("Seeding all attendees...")
    seed_all_attendees()
    
    print("Seeding all organisers...")
    seed_all_organisers()
    
    print("Seeding perks...")
    seed_perks()
    
    print("Seeding all registrations...")
    seed_all_registrations()
    
    print("Database seeding completed!")

if __name__ == "__main__":
    seed_database() 