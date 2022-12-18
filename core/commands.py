from typing import Any

from tabulate import tabulate

from .exceptions import ProgramExit
from .models import OperationType
from . import utils
from . import validators


class Commands:
	"""Класс для хранения всех исполняемых команд."""

	@staticmethod
	def exit() -> None:
		"""
		Type this to exit the program.
		"""
		print(utils.BYE_MESSAGE)
		raise ProgramExit

	@staticmethod
	def deposit(client: Any, amount: Any, description: Any) -> None:
		"""
		This command is used to deposit money to the client's account.
		"""
		try:
			validators.validate_change_balance_input(client, amount, description)
		except ValueError as e:
			print(f'Unsuccessful operation: {e}.')
			return
		resp = utils.change_balance(client, amount, description, OperationType.DEPOSIT)
		print(resp)

	@staticmethod
	def withdraw(client: Any, amount: Any, description: Any) -> None:
		"""Команда для вызова операции списания средств с счёта клиента."""
		try:
			validators.validate_change_balance_input(client, amount, description)
		except ValueError as e:
			print(f'Unsuccessful operation: {e}.')
			return

		resp = utils.change_balance(client, amount, description, OperationType.WITHDRAW)
		print(resp)

	@staticmethod
	def show_bank_statement(client: Any, since: Any = None, till: Any = None) -> None:
		"""Команда для вызова операции показа банковского выписки клиента."""
		try:
			validators.validate_show_bank_statement_input(client, since, till)
		except ValueError as e:
			print(f'Unsuccessful operation: {e}.')
			return

		operations = utils.retrieve_user_operations(client, since, till)
		if not operations:
			print('No operations found.')
			return

		headers = ('Date', 'Description', 'Withdrawals', 'Deposits', 'Balance')
		data = [[
			op.created.strftime('%d.%m.%Y %H:%M:%S'),
			op.description,
			op.amount if op.type_ == OperationType.WITHDRAW else '',
			op.amount if op.type_ == OperationType.DEPOSIT else '',
			op.balance,
		] for op in operations]
		print(tabulate(data, headers=headers, tablefmt='psql'))
