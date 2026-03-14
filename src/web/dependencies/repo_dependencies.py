from fastapi import Depends

from app.transaction_repo import TransactionRepository
from web.dependencies.db_dependency import DBDependency


def get_transaction_repo(db: DBDependency = Depends(DBDependency)):
    return TransactionRepository(db.db_session())

