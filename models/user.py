from sqlalchemy import Column, Integer, String, Boolean, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


user_roles = Table(
    "user_roles", Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("role_id", Integer, ForeignKey("roles.id"))
)

user_permissions = Table(
    "user_permissions", Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("permission_id", Integer, ForeignKey("permissions.id"))
)

role_permissions = Table(
    "role_permissions", Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id")),
    Column("permission_id", Integer, ForeignKey("permissions.id"))
)


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")
    users = relationship("User", secondary=user_permissions, back_populates="permissions")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")
    users = relationship("User", secondary=user_roles, back_populates="roles")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    avatar = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    roles = relationship("Role", secondary=user_roles, back_populates="users")
    permissions = relationship("Permission", secondary=user_permissions, back_populates="users")
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")