"""
One-time script to clear old placeholder destinations and re-seed with real demo data.
Run from the TravelUp project root inside the venv:
    python fix_destinations.py
"""
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from core.config import settings
from models.destination import Destination

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

engine = create_engine(settings.DATABASE_URL)
db = Session(bind=engine)

print("Deleting all existing destinations...")
db.query(Destination).delete()
db.commit()

print(f"Seeding {len(DEMO_DESTINATIONS)} demo destinations...")
for d in DEMO_DESTINATIONS:
    db.add(Destination(**d))
db.commit()
db.close()
print("Done! Refresh your browser.")
