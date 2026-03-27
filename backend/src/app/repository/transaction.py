from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate


# create a new transaction
def create_transaction(db: Session, transaction: TransactionCreate):
    new_transaction = Transaction(
        amount=transaction.amount,
        description=transaction.description,
        user_id=transaction.user_id,
        category_id=transaction.category_id,
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction


# get one transaction by id
def get_transaction_by_id(db: Session, transaction_id: int):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    return transaction


# get all transactions
def get_all_transactions(db: Session):
    transactions = db.query(Transaction).all()
    return transactions


# update a transaction
def update_transaction(db: Session, transaction_id: int, updated_data: dict):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if transaction is None:
        return None

    for key, value in updated_data.items():
        setattr(transaction, key, value)

    db.commit()
    db.refresh(transaction)

    return transaction


# delete a transaction
def delete_transaction(db: Session, transaction_id: int):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if transaction is None:
        return None

    db.delete(transaction)
    db.commit()

    return transaction