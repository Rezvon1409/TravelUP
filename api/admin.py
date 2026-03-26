from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from database import get_db
from core.permissions import get_admin_user
from models.user import User, Role, Permission
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["Admin"])


class SetRoleSchema(BaseModel):
    user_id: int
    role_id: int


class SetPermissionSchema(BaseModel):
    user_id: int
    permission_ids: list[int]



@router.get("/roles")
async def get_roles(user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    return db.query(Role).all()


@router.get("/permissions")
async def get_permissions(user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    return db.query(Permission).all()


@router.post("/set-role")
async def set_role(data: SetRoleSchema, user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    target_user = db.query(User).filter(User.id == data.user_id).first()
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    role = db.query(Role).filter(Role.id == data.role_id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    if role not in target_user.roles:
        target_user.roles.append(role)
        db.commit()

    return {"msg": f"Role '{role.name}' added to user '{target_user.username}'"}


@router.post("/set-permissions")
async def set_permissions(data: SetPermissionSchema, user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    target_user = db.query(User).options(selectinload(User.permissions)).filter(User.id == data.user_id).first()
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    permissions = db.query(Permission).filter(Permission.id.in_(data.permission_ids)).all()
    if not permissions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permissions not found")

    for perm in permissions:
        if perm not in target_user.permissions:
            target_user.permissions.append(perm)

    db.commit()
    return {"msg": f"Permissions added to user '{target_user.username}'"}



@router.post("/make-admin")
async def make_admin(user_id: int, user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    
    target.is_admin = True
    
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    if admin_role and admin_role not in target.roles:
        target.roles.append(admin_role)
    
    db.commit()
    return {"msg": f"{target.username} is now admin"}

@router.get("/users")
async def get_users(user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    users = db.query(User).options(selectinload(User.roles),selectinload(User.permissions)).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "is_admin": u.is_admin,
            "roles": [r.name for r in u.roles],
            "permissions": [p.name for p in u.permissions]
        }
        for u in users
    ]