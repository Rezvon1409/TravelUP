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

engine = create_engine(settings.DATABASE_URL)

models = [User, Booking, Destination, Review, Payment, UserProfile]
actions = ["read", "create", "update", "delete"]
role_names = ["admin", "moderator", "user"]


def seed_permissions(db: Session):
    for model in models:
        for action in actions:
            name = f"{model.__tablename__}:{action}"
            if not db.query(Permission).filter(Permission.name == name).first():
                db.add(Permission(name=name))
    db.commit()
    print("Permissions created!")


def seed_roles(db: Session):
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
    db.commit()
    print("Admin created!")


def run_seeds():
    db = Session(bind=engine)
    seed_permissions(db)
    seed_roles(db)
    seed_admin(db)
    db.close()


if __name__ == "__main__":
    run_seeds()