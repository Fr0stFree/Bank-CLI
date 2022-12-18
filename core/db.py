import datetime as dt
from collections import deque
from decimal import Decimal
from typing import Optional

from .exceptions import NotEnoughMoneyError
from .models import User, OperationType, Currency, Operation


class Singleton:
    """Реализация паттерна Singleton"""
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class Users(Singleton):
	"""Класс для хранения всех пользователей."""
	_users: dict[str, User] = {}

	def create(self, name: str) -> User:
		"""Метод для создания экземпляра пользователя и занесения его в таблицу."""
		user = User(name)
		self._users[name] = User(name)
		return user

	def get(self, name: str) -> Optional[User]:
		"""Метод для получения пользователя по его имени."""
		return self._users.get(name)

	def get_or_create(self, name: str) -> tuple[User, bool]:
		"""Метод для получения пользователя по его имени."""
		user = self._users.get(name)
		if user is None:
			return self.create(name), True
		return user, False


class Operations(Singleton):
	"""Класс для хранения всех операций."""
	_operations: dict[str, deque[Operation]] = {}

	def list(self, user_name: str, since: dt.datetime = None,
			till: dt.datetime = None) -> deque[Operation]:
		"""Метод для получения операций по имени пользователя."""
		operations = self._operations.get(user_name, deque())
		if since is None and till is None:
			return operations
		if since is None:
			since = dt.datetime.min
		if till is None:
			till = dt.datetime.max
		return deque(filter(lambda x: since <= x.created <= till, operations))


	def create(self, user_name: str, amount: Decimal, currency: Currency,
			   description: str, type_: OperationType) -> Operation:
		"""Метод для создания операции."""
		is_exist = user_name in self._operations
		if not is_exist:
			self._operations[user_name] = deque()

		#  Расчёт баланса для операции
		before = Decimal(0) if not is_exist else self._operations[user_name][-1].balance
		balance = before + amount if type_ == OperationType.DEPOSIT else before - amount
		if balance < 0:
			raise NotEnoughMoneyError

		operation = Operation(user_name=user_name, amount=amount, balance=balance,
							  currency=currency, description=description, type_=type_,
							  created=dt.datetime.now())
		self._operations[user_name].append(operation)
		return operation
