from fastapi import APIRouter, Depends

from app.transaction_repo import TransactionRepository
from app.transaction_service import TransactionService
from schemas.search import SearchRequest
from schemas.transactions import TransactionData
from web.dependencies.repo_dependencies import get_transaction_repo
from web.dependencies.service_dependencies import get_transaction_service
from web.signed_api_route import SignedAPIRoute

router = APIRouter(prefix="/messages", route_class=SignedAPIRoute)

@router.post(
    "/outgoing",
    response_model=TransactionData,
)
def outgoing_messages(
        search_request: SearchRequest,
        transaction_service: TransactionService = Depends(get_transaction_service),
):
    found_transactions = transaction_service.search_transactions(search_request)

    return TransactionData(
        transactions=found_transactions,
        count=len(found_transactions),
    )

@router.post(
    "/incoming",
    response_model=TransactionData,
)
def incoming_messages(
        transaction_data: TransactionData,
        transaction_service: TransactionService = Depends(get_transaction_service),
):
    response_transactions = transaction_service.save_and_response_transactions(transaction_data.transactions)

    return TransactionData(
        transactions=response_transactions,
        count=len(response_transactions),
    )