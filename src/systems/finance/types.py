from enum import Enum


class TransactionType(Enum):
    INCOME = "income"
    EXPENSIVE = "expensive"


class OperationType(Enum):
    INCOME = "income"
    EXPENSIVE = "expensive"
    TRANSFER = "transfer"
