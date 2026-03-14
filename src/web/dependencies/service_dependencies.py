from fastapi import Depends

from app.transaction_repo import TransactionRepository
from app.transaction_service import TransactionService
from web.dependencies.repo_dependencies import get_transaction_repo


def get_transaction_service(transaction_repository: TransactionRepository = Depends(get_transaction_repo)):
    return TransactionService(transaction_repository)

