import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import count

from constants import SystemTypes
from models import Transaction as DBTransaction
from schemas.transactions import Transaction


class TransactionRepository:
    """Repository for working with transactions in the database.

    Encapsulates data access: saving, searching, and counting transactions.
    """
    def __init__(self, session: Session):
        self._session = session

    def save_transaction(self, transaction: Transaction):
        """Save a transaction to the database.
        """
        transaction_dump = transaction.model_dump(exclude={"metadata"}, by_alias=False)
        transaction_dump.update(
            {
                "transaction_metadata": transaction.metadata,
                "message_receiver_batch": transaction.data.receiver_batch,
            }
        )
        with self._session.begin():
            self._session.add(DBTransaction(**transaction_dump))

    def  search_transactions(
            self,
            start_dt: datetime.datetime,
            end_dt: datetime.datetime,
            limit: int,
            offset: int,
    ):
        """Search transactions by date range filtered by receiver.

        Returns transactions for SYSTEM_A, sorted by time,
        with pagination applied (limit/offset).
        """
        stmt = (
            select(DBTransaction)
            .where(
                DBTransaction.message_receiver_batch == SystemTypes.SYSTEM_A,
                DBTransaction.transaction_time.between(start_dt, end_dt)
            )
            .order_by(DBTransaction.transaction_time)
            .limit(limit)
            .offset(offset)
        )

        with self._session.begin():
            db_transactions = self._session.scalars(stmt).all()

        transactions = []
        for db_transaction in db_transactions:
            db_transaction: DBTransaction
            db_transaction.transaction_time = db_transaction.transaction_time.replace(
                tzinfo=datetime.timezone.utc,
            )

            transactions.append(
                Transaction.model_validate(db_transaction, extra="ignore", from_attributes=True)
            )
        return transactions

    def transactions_count(self) -> int:
        """Return total number of transactions in the database."""
        stmt = (
            select(count(DBTransaction.id))
        )
        with self._session.begin():
            return self._session.scalar(stmt)
