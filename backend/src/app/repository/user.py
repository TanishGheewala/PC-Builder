from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate


# create a new user
def create_user(db: Session, user: UserCreate):
    new_user = User(name=user.name, email=user.email, password=user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# get one user by id
def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    return user


# get all users
def get_all_users(db: Session):
    users = db.query(User).all()
    return users


# update a user's information
def update_user(db: Session, user_id: int, updated_data: dict):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        return None

    for key, value in updated_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


# delete a user
def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        return None

    db.delete(user)
    db.commit()

    return user
