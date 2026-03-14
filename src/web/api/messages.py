import logging

from fastapi import APIRouter, Depends
from pydantic import ValidationError
from starlette import status
from starlette.exceptions import HTTPException

from app.transaction_service import TransactionService
from schemas.search import SearchRequest
from schemas.transactions import TransactionData
from web.dependencies.service_dependencies import get_transaction_service
from web.signed_api_route import SignedAPIRoute


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/messages", route_class=SignedAPIRoute)

@router.post(
    "/outgoing",
    response_model=TransactionData,
)
def outgoing_messages(
        search_request: SearchRequest,
        transaction_service: TransactionService = Depends(get_transaction_service),
):
    """Get incoming messages for System A.

    Returns list of transactions with messages addressed to System A
    for the specified time period with pagination.
    """
    try:
        found_transactions = transaction_service.search_transactions(search_request)
    except ValidationError:
        logger.exception("Validation Error")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    """Send messages from System A to System B.

    Saves incoming transactions and generates response receipts (type 215)
    for all messages except receipts.
    """
    try:
        response_transactions = transaction_service.save_and_response_transactions(transaction_data.transactions)
    except ValidationError:
        logger.exception("Validation Error")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return TransactionData(
        transactions=response_transactions,
        count=len(response_transactions),
    )