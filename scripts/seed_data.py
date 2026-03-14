from app.transaction_repo import TransactionRepository
from app.transaction_service import TransactionService
from schemas.transactions import Transaction
from web.dependencies.db_dependency import DBDependency


def seed_data(db_dependency: DBDependency):
    transaction_repo = TransactionRepository(db_dependency.db_session())

    if transaction_repo.transactions_count() == 0:
        transaction_service = TransactionService(transaction_repo)
        with open("data/seed_transaction.json") as file:
            seed_json = file.read()

        transaction = Transaction.model_validate_json(seed_json)
        transaction_service.save_and_response_transactions([transaction])
