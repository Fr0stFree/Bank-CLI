import datetime as dt
from decimal import Decimal
from enum import Enum
from typing import NamedTuple


class OperationType(Enum):
    """Enum класс для типа операции."""
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'


class Currency(Enum):
    """Enum класс для валюты."""
    USD = '$'


class Operation(NamedTuple):
    """Операция."""
    user_name: str  # Связь с пользователем. По этому ключу будем хранить операции.
    amount: Decimal
    balance: Decimal
    currency: Currency
    description: str
    type_: OperationType
    created: dt.datetime

    def __repr__(self):
        return f'Operation(type={self.type_}, user_name={self.user_name}, dt={self.created}, ' \
               f'amount={self.amount}, currency={self.currency}, balance={self.balance})'


class User:
    """Класс пользователя."""
    def __init__(self, name: str, currency: Currency = Currency.USD):
        self._name = name
        self._currency = currency

    __slots__ = ('_name', '_currency')

    def __str__(self):
        return f'{self._name}'

    def __repr__(self):
        return f'(name={self._name}, currency={self._currency})'

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def currency(self) -> Currency:
        return self._currency

    @currency.setter
    def currency(self, value: Currency):
        self._currency = value
