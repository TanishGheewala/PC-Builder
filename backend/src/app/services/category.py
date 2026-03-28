from sqlalchemy.orm import Session

from app.repository.category import (
    create_category as repo_create_category,
    delete_category as repo_delete_category,
    get_all_categories as repo_get_all_categories,
    get_category_by_id as repo_get_category_by_id,
    update_category as repo_update_category,
)
from app.schemas.category import CategoryCreate, CategoryUpdate


def create_category(db: Session, category: CategoryCreate):
    return repo_create_category(db, category)


def get_all_categories(db: Session):
    return repo_get_all_categories(db)


def get_category_by_id(db: Session, category_id: int):
    return repo_get_category_by_id(db, category_id)


def update_category(db: Session, category_id: int, category_data: CategoryUpdate):
    return repo_update_category(
        db, category_id, category_data.model_dump(exclude_unset=True)
    )


def delete_category(db: Session, category_id: int):
    return repo_delete_category(db, category_id)
