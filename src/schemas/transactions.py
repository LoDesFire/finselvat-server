import enum
from decimal import Decimal
from typing import Optional, Union, TypeVar, Generic, Annotated, Self, Any

from pydantic import UUID4, Field, Tag, Discriminator, Base64Bytes, model_validator, field_validator, AliasChoices
from pydantic_core.core_schema import ValidationInfo, ValidatorFunctionWrapHandler

from constants import InfoMessageType
from schemas.mixins import DataValidatorsMixin, SignatureValidatorMixin

from src.schemas.base_schema import BaseSchema, UTCDateTime
from utils.base64_utils import encode_bytes_base64

from utils.hash_utils import sha256_hash

MessageDataT = TypeVar("MessageDataT")


class Message(BaseSchema, DataValidatorsMixin, Generic[MessageDataT]):
    data: MessageDataT
    sender_batch: str
    receiver_batch: str
    info_message_type: InfoMessageType
    message_time: UTCDateTime
    chain_guid: UUID4
    previous_transaction_hash: Optional[str]
    metadata: Optional[str]


class Tax(BaseSchema):
    number: str
    name_tax: str
    amount: Decimal
    penny_amount: Decimal


class Obligation(BaseSchema):
    type: int
    start_date: UTCDateTime
    end_date: UTCDateTime
    act_date: UTCDateTime
    act_number: str
    taxs: list[Tax]


class IssuedGuaranteeMessageData(BaseSchema):
    information_type: int = Field(InfoMessageType.ISSUED_GUARANTEE, frozen=True)
    information_type_string: str
    number: str
    issued_date: UTCDateTime
    guarantor: str
    beneficiary: str
    principal: str
    obligations: list[Obligation]
    start_date: UTCDateTime
    end_date: UTCDateTime
    currency_code: str
    currency_name: str
    amount: Decimal
    revokation_info: str
    claim_right_transfer: str
    payment_period: str
    signer_name: str
    authorized_position: str
    bank_guarantee_hash: str


class AcceptedGuaranteeMessageData(BaseSchema, SignatureValidatorMixin):
    name: str
    bank_guarantee_hash: str
    sign: Base64Bytes
    signer_cert: Base64Bytes


class DeniedGuaranteeMessageData(BaseSchema, SignatureValidatorMixin):
    name: str
    bank_guarantee_hash: str
    sign: Base64Bytes
    signer_cert: Base64Bytes
    reason: str


class ReceivedGuaranteeMessageData(BaseSchema):
    bank_guarantee_hash: str


TransactionDataType = Annotated[
    Union[
        Annotated[Message[IssuedGuaranteeMessageData], Tag(str(InfoMessageType.ISSUED_GUARANTEE))],
        Annotated[Message[AcceptedGuaranteeMessageData], Tag(str(InfoMessageType.ACCEPTED_GUARANTEE))],
        Annotated[Message[DeniedGuaranteeMessageData], Tag(str(InfoMessageType.DENIED_GUARANTEE))],
        Annotated[Message[ReceivedGuaranteeMessageData], Tag(str(InfoMessageType.RECEIVED_GUARANTEE))],
    ],
    Discriminator(lambda v: str(v["InfoMessageType"]) if isinstance(v, dict) else str(v.info_message_type)),
]


class Transaction(BaseSchema, DataValidatorsMixin, SignatureValidatorMixin):
    transaction_type: int
    data: TransactionDataType
    hash: str
    sign: Base64Bytes
    signer_cert: Base64Bytes
    transaction_time: UTCDateTime
    metadata: Optional[str] = Field(..., validation_alias=AliasChoices("Metadata", "transaction_metadata"))
    transaction_in: Optional[str]
    transaction_out: Optional[str]

    class ContextKeys(enum.Enum):
        NEED_NEW_HASH_AND_SIGN = 0

    @field_validator('sign', mode='wrap')
    @classmethod
    def validate_sign_wrap(cls, value: Any, handler: ValidatorFunctionWrapHandler, info: ValidationInfo) -> str:
        if info.context is None:
            need_new_hash = False
        else:
            need_new_hash = info.context.get(cls.ContextKeys.NEED_NEW_HASH_AND_SIGN, False)

        if not need_new_hash:
            return handler(value)

        return value


    @model_validator(mode='after')
    def validate_model_hash(self, info: ValidationInfo) -> Self:
        if info.context is None:
            need_new_hash = False
        else:
            need_new_hash = info.context.get(self.ContextKeys.NEED_NEW_HASH_AND_SIGN, False)

        transaction_copy = self.model_copy()
        transaction_copy.sign = b''
        transaction_copy.hash = ""
        calculated_hash = sha256_hash(transaction_copy.model_dump_json().encode("utf-8"))

        if not need_new_hash:
            if calculated_hash.hex().upper() != self.hash.upper():
                raise ValueError(f'Transaction hash `{self.hash}` does not match')
        else:
            self.hash = calculated_hash.hex().upper()
            self.sign = encode_bytes_base64(calculated_hash)

        return self


class TransactionData(BaseSchema):
    transactions: list[Transaction]
    count: int
