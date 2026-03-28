from sqlalchemy.orm import Session

from app.repository.transaction import (
    create_transaction as repo_create_transaction,
    delete_transaction as repo_delete_transaction,
    get_all_transactions as repo_get_all_transactions,
    get_transaction_by_id as repo_get_transaction_by_id,
    update_transaction as repo_update_transaction,
)
from app.schemas.transaction import TransactionCreate, TransactionUpdate


def create_transaction(db: Session, transaction: TransactionCreate):
    return repo_create_transaction(db, transaction)


def get_all_transactions(db: Session):
    return repo_get_all_transactions(db)


def get_transaction_by_id(db: Session, transaction_id: int):
    return repo_get_transaction_by_id(db, transaction_id)


def update_transaction(
    db: Session,
    transaction_id: int,
    transaction_data: TransactionUpdate,
):
    return repo_update_transaction(
        db,
        transaction_id,
        transaction_data.model_dump(exclude_unset=True),
    )


def delete_transaction(db: Session, transaction_id: int):
    return repo_delete_transaction(db, transaction_id)
