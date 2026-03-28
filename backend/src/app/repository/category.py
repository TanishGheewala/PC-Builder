from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate


def create_category(db: Session, category: CategoryCreate):
    new_category = Category(
        name=category.name,
        user_id=category.user_id,
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


def get_category_by_id(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    return category


def get_all_categories(db: Session):
    categories = db.query(Category).all()
    return categories


def update_category(db: Session, category_id: int, updated_data: dict):
    category = db.query(Category).filter(Category.id == category_id).first()

    if category is None:
        return None

    for key, value in updated_data.items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)

    return category


def delete_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()

    if category is None:
        return None

    db.delete(category)
    db.commit()

    return category
