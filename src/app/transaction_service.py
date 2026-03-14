import datetime

from app.transaction_repo import TransactionRepository
from constants import InfoMessageType, TransactionType, SystemTypes
from schemas.search import SearchRequest
from schemas.transactions import Transaction, ReceivedGuaranteeMessageData, Message
from utils.base64_utils import encode_str_base64


class TransactionService:
    def __init__(self, transaction_repository: TransactionRepository):
        self._transaction_repo = transaction_repository

    def save_and_response_transactions(self, transactions: list[Transaction]) -> list[Transaction]:
        response_transactions: list[Transaction] = []

        for transaction in transactions:
            self._transaction_repo.save_transaction(transaction)

            if transaction.data.info_message_type == InfoMessageType.RECEIVED_GUARANTEE:
                continue

            response_transactions.append(
                Transaction.model_validate(
                    obj=dict(
                        transaction_type=TransactionType.INFO_MESSAGE,
                        data=Message[ReceivedGuaranteeMessageData](
                            data=ReceivedGuaranteeMessageData(
                                bank_guarantee_hash=transaction.data.data.bank_guarantee_hash,
                            ),
                            sender_batch=SystemTypes.SYSTEM_B,
                            receiver_batch=SystemTypes.SYSTEM_A,
                            info_message_type=InfoMessageType.RECEIVED_GUARANTEE,
                            message_time=datetime.datetime.now(tz=datetime.timezone.utc),
                            chain_guid=transaction.data.chain_guid,
                            previous_transaction_hash=None,
                            metadata=None,
                        ),
                        hash="",
                        sign=b'',
                        signer_cert=encode_str_base64(SystemTypes.SYSTEM_B),
                        transaction_time=datetime.datetime.now(tz=datetime.timezone.utc),
                        metadata=None,
                        transaction_in=None,
                        transaction_out=None,
                    ),
                    context={Transaction.ContextKeys.NEED_NEW_HASH_AND_SIGN: True},
                )
            )

        return response_transactions

    def search_transactions(self, search_request: SearchRequest) -> list[Transaction]:
        return self._transaction_repo.search_transactions(
            search_request.start_date,
            search_request.end_date,
            limit=search_request.limit,
            offset=search_request.offset,
        )