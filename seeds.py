from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from core.config import settings
from core.security import hash_password
from models.user import User, Role, Permission
from models.booking import Booking
from models.destination import Destination
from models.review import Review
from models.payment import Payment
from models.profile import UserProfile
from database import Base, engine

def seed_permissions(db: Session):
    models = [User, Booking, Destination, Review, Payment, UserProfile]
    actions = ["read", "create", "update", "delete"]
    for model in models:
        for action in actions:
            name = f"{model.__tablename__}:{action}"
            if not db.query(Permission).filter(Permission.name == name).first():
                db.add(Permission(name=name))
    db.commit()
    print("Permissions created!")

def seed_roles(db: Session):
    role_names = ["admin", "moderator", "user"]
    for name in role_names:
        if not db.query(Role).filter(Role.name == name).first():
            db.add(Role(name=name))
    db.commit()
    print("Roles created!")

def seed_admin(db: Session):
    if db.query(User).filter(User.username == "admin").first():
        print("Admin already exists!")
        return

    admin = User(username="admin", password_hash=hash_password("admin123"), is_admin=True)
    db.add(admin)
    db.commit()
    db.refresh(admin)

    admin.roles.append(db.query(Role).filter(Role.name == "admin").first())
    admin.permissions.extend(db.query(Permission).all())
    

    profile = UserProfile(
        user_id=admin.id,
        first_name="Stellar",
        last_name="Admin",
        email="admin@travelup.app",
        bio="Master of the Cosmic Travel Nebula.",
        theme="light"
    )
    db.add(profile)
    
    db.commit()
    print("Admin created with profile!")

DEMO_DESTINATIONS = [
    {
        "title": "Eiffel Tower & Parisian Charm",
        "description": "Stroll along the Seine, climb the iconic Eiffel Tower, and indulge in world-class cuisine in the City of Light.",
        "country": "France", "city": "Paris", "rating": 4.9,
        "cover_image": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800&auto=format&fit=crop"
    },
    {
        "title": "Santorini Sunset Escape",
        "description": "Experience breathtaking sunsets over the caldera, white-washed villages, and crystal-clear Aegean waters.",
        "country": "Greece", "city": "Santorini", "rating": 4.8,
        "cover_image": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=800&auto=format&fit=crop"
    },
    {
        "title": "Tokyo Neon & Tradition",
        "description": "Discover ancient temples next to futuristic skyscrapers, world-class sushi, and vibrant street culture.",
        "country": "Japan", "city": "Tokyo", "rating": 4.8,
        "cover_image": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800&auto=format&fit=crop"
    },
    {
        "title": "Bali Spiritual Retreat",
        "description": "Find inner peace among lush rice terraces, sacred temples, and pristine beaches on the Island of the Gods.",
        "country": "Indonesia", "city": "Bali", "rating": 4.7,
        "cover_image": "https://images.unsplash.com/photo-1537953773345-d172ccf13cf1?w=800&auto=format&fit=crop"
    },
    {
        "title": "New York City Adventure",
        "description": "The city that never sleeps — Times Square, Central Park, world-class museums, and a skyline like no other.",
        "country": "USA", "city": "New York", "rating": 4.7,
        "cover_image": "https://images.unsplash.com/photo-1485871981521-5b1fd3805eee?w=800&auto=format&fit=crop"
    },
    {
        "title": "Safari in the Serengeti",
        "description": "Witness the Great Migration and encounter the Big Five in their natural habitat on an unforgettable savanna safari.",
        "country": "Tanzania", "city": "Serengeti", "rating": 4.9,
        "cover_image": "https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=800&auto=format&fit=crop"
    },
    {
        "title": "Machu Picchu Mysteries",
        "description": "Trek through the Andes and discover the ancient Incan citadel hidden among the clouds at 2,430 metres.",
        "country": "Peru", "city": "Cusco", "rating": 4.8,
        "cover_image": "https://images.unsplash.com/photo-1526392060635-9d6019884377?w=800&auto=format&fit=crop"
    },
    {
        "title": "Dubai Luxury Experience",
        "description": "From the world's tallest building to golden deserts and ultra-luxury resorts, Dubai is unlike anywhere on Earth.",
        "country": "UAE", "city": "Dubai", "rating": 4.6,
        "cover_image": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800&auto=format&fit=crop"
    },
    {
        "title": "Amalfi Coast Road Trip",
        "description": "Drive along dramatic cliff-hugging roads, visit colourful fishing villages, and savour fresh limoncello.",
        "country": "Italy", "city": "Amalfi", "rating": 4.8,
        "cover_image": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800&auto=format&fit=crop"
    },
    {
        "title": "Maldives Overwater Bliss",
        "description": "Wake up above turquoise lagoons in a private overwater bungalow and dive into vibrant coral reefs.",
        "country": "Maldives", "city": "Malé", "rating": 5.0,
        "cover_image": "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800&auto=format&fit=crop"
    },
]

def seed_destinations(db: Session):
    if db.query(Destination).count() > 0:
        print("Destinations already seeded!")
        return
    for d in DEMO_DESTINATIONS:
        db.add(Destination(**d))
    db.commit()
    print(f"Seeded {len(DEMO_DESTINATIONS)} demo destinations!")

def run_seeds():
   
    Base.metadata.create_all(bind=engine)
    db = Session(bind=engine)
    seed_permissions(db)
    seed_roles(db)
    seed_admin(db)
    seed_destinations(db)
    db.close()

if __name__ == "__main__":
    run_seeds()