from types import NoneType
from typing import Any
import datetime as dt

from . import settings


def validate_change_balance_input(client: Any, amount: Any, description: Any) -> None:
    validate_username(client)
    validate_amount(amount)
    validate_description(description)


def validate_show_bank_statement_input(client: Any, since: Any, till: Any) -> None:
    validate_username(client)
    validate_datetime(since, nullable=True)
    validate_datetime(till, nullable=True)
    validate_datetime_range(since, till)


def validate_username(username: Any) -> None:
	"""Валидация ввода имени клиента."""
	if not isinstance(username, str):
		raise ValueError('Client name must be a string.')
	if len(username) > settings.MAX_CLIENT_NAME_LENGTH:
		raise ValueError(
			f'Client name must be less than {settings.MAX_CLIENT_NAME_LENGTH} characters.'
		)
	if not username:
		raise ValueError('Client name must not be empty.')


def validate_amount(amount: Any) -> None:
	"""Валидация ввода суммы."""
	if not isinstance(amount, (int, float)):
		raise ValueError('Amount must be a number.')
	if amount <= 0:
		raise ValueError('Amount must be greater than zero.')


def validate_description(description: Any) -> None:
	"""Валидация ввода описания операции."""
	if not isinstance(description, str):
		raise ValueError('Description must be a string.')
	if len(description) > settings.MAX_OPERATION_DESCRIPTION_LENGTH:
		raise ValueError(
			f'Description must be less than {settings.MAX_OPERATION_DESCRIPTION_LENGTH} characters.'
		)
	if not description:
		raise ValueError('Description must not be empty.')


def validate_datetime(datetime: Any, nullable: bool) -> None:
	"""Валидация ввода даты."""
	if nullable and datetime is None:
		return
	if not isinstance(datetime, str):
		raise ValueError('Date must be a string. "Example: 2019-01-31 00:00:00"')
	try:
		dt.datetime.strptime(datetime, settings.DATETIME_FORMAT)
	except ValueError:
		raise ValueError(
			f'Incorrect date format. Must be "{settings.DATETIME_FORMAT}". '
			'Example: "2019-01-31 00:00:00"'
		)


def validate_datetime_range(since: str, till: str) -> None:
	"""Валидация ввода диапазона дат."""
	if since and till:
		since = dt.datetime.strptime(since, settings.DATETIME_FORMAT)
		till = dt.datetime.strptime(till, settings.DATETIME_FORMAT)
		if since > till:
			raise ValueError('Start date must be less than end date.')
