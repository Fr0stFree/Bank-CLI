import datetime as dt
from collections import deque
from decimal import Decimal
from typing import Union, Optional

from . import settings
from .models import OperationType, Operation
from .db import Users, Operations
from .exceptions import NotEnoughMoneyError


HELLO_MESSAGE = 'Dear user, welcome to the Bank App CLI!\nTo get all commands, type "help".'
BYE_MESSAGE = '\nSystem exit. Goodbye!'


def change_balance(client: str, amount: Union[float, int], description: str,
                   type_: OperationType) -> str:
    """Функция для изменения баланса пользователя и создания экземпляра операции."""
    users, operations = Users(), Operations()
    user, _ = users.get_or_create(client)
    amount = Decimal(amount)
    try:
        operations.create(user.name, amount, user.currency, description, type_)
    except NotEnoughMoneyError:
        return f'Operation failed. Not enough money on the account.'
    return f'Operation {type_.name} for {amount:.2f} {user.currency.value} was successful.'


def retrieve_user_operations(client: str, since: Optional[str],
                             till: Optional[str]) -> deque[Operation]:
    """Функция для получения операций пользователя за определенный период."""
    users, operations = Users(), Operations()
    user = users.get(client)
    if user is None:
        return deque()

    since = dt.datetime.strptime(since, settings.DATETIME_FORMAT) if since else None
    till = dt.datetime.strptime(till, settings.DATETIME_FORMAT) if till else None
    return operations.list(user_name=user.name, since=since, till=till)
