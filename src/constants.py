import enum


class InfoMessageType(enum.IntEnum):
    ISSUED_GUARANTEE = 201
    ACCEPTED_GUARANTEE = 202
    DENIED_GUARANTEE = 203
    RECEIVED_GUARANTEE = 215


class TransactionType(enum.IntEnum):
    INFO_MESSAGE = 9
    GUARANTEE_MESSAGE = 18

class SystemTypes(enum.StrEnum):
    SYSTEM_A = "SYSTEM_A"
    SYSTEM_B = "SYSTEM_B"