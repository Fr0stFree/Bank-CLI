import subprocess
import os
from typing import Optional

from core import utils


ENTRY_POINT = os.path.join(os.path.dirname(__file__), 'main.py')


def test_user_able_to_run_and_exit_program():
	"""Тест проверяет, что пользователь может запустить программу и выйти из нее."""
	process = _run_cli(data_input='exit')
	assert process.returncode == 0
	assert utils.BYE_MESSAGE in process.stdout


def test_user_see_success_message_after_deposit():
	"""Тест проверяет, что пользователь видит сообщение об успешной операции."""
	name, income, desc = 'John', 100, 'salary'
	test_input = _type_in_deposit_command(name, income, desc) + 'exit'
	process = _run_cli(test_input)
	assert process.returncode == 0
	assert f'Operation DEPOSIT for {income}.00$ for {name} was successful' in process.stdout


def test_user_unable_to_withdraw_more_than_he_has():
	"""Тест проверяет, что пользователь не может списать с счета больше, чем у него есть."""
	name, income, desc = 'John', 100, 'salary'
	outcome = income + 1
	test_input = _type_in_deposit_command(name, income, desc) + \
				 _type_in_withdraw_command(name, outcome, desc) + 'exit'
	process = _run_cli(test_input)
	assert process.returncode == 0
	assert f'Not enough money on the account' in process.stdout
	assert f'Operation WITHDRAW for {outcome}.00$ for {name} was successful' not in process.stdout


def test_user_balance_calculated_correctly():
	"""Тест проверяет, что баланс пользователя рассчитывается правильно."""
	name, desc = 'John', 'test_description'
	incomes = (12, 245.23, 512.50)
	outcomes = (62.2, 250.4, 1.02)
	expected_balance = round(sum(incomes) - sum(outcomes), 2)

	test_input = [_type_in_deposit_command(name, income, desc) for income in incomes] + \
				 [_type_in_withdraw_command(name, outcome, desc) for outcome in outcomes] + \
				 [_type_in_show_balance_command(name), 'exit']

	process = _run_cli(''.join(test_input))
	assert process.returncode == 0
	assert str(expected_balance) in process.stdout


def test_different_users_wont_be_able_to_see_each_other_balance():
	"""Тест проверяет, что пользователи не смогут увидеть баланс друг друга."""
	name1, name2 = 'John', 'Jane'
	income, desc = 999, 'Stolen money'
	test_input = _type_in_deposit_command(name1, income, desc) + \
				 _type_in_show_balance_command(name2) + 'exit'
	process = _run_cli(test_input)
	assert process.returncode == 0
	assert 'No operations found' in process.stdout
	assert desc not in process.stdout


def test_deposit_wont_be_created_if_client_name_is_not_provided():
	"""Тест проверяет, что операция внесения денег не будет создана, если не указано имя клиента."""
	amount, desc = 100, 'salary'
	test_input = _type_in_deposit_command('', amount, desc) + 'exit'
	process = _run_cli(test_input)
	assert process.returncode == 0
	assert 'Unsuccessful operation: Client name must not be empty' in process.stdout
	assert 'was successful' not in process.stdout


def test_deposit_wont_be_created_if_amount_is_not_provided():
	"""Тест проверяет, что операция внесения денег не будет создана, если не указана сумма."""
	name, desc = 'John', 'salary'
	test_input = _type_in_deposit_command(name, 0, desc) + 'exit'
	process = _run_cli(test_input)
	assert process.returncode == 0
	assert 'Unsuccessful operation: Amount must be greater than zero' in process.stdout
	assert 'was successful' not in process.stdout


def test_deposit_wont_be_created_if_description_is_not_provided():
	"""Тест проверяет, что операция внесения денег не будет создана, если не указано описание."""
	name, amount = 'John', 100
	test_input = _type_in_deposit_command(name, amount, '') + 'exit'
	process = _run_cli(test_input)
	assert process.returncode == 0
	assert 'Unsuccessful operation: Description must not be empty' in process.stdout
	assert 'was successful' not in process.stdout


def test_withdraw_wont_be_created_if_client_name_is_not_provided():
	"""Тест проверяет, что операция списания денег не будет создана, если не указано имя клиента."""
	amount, desc, name = 150, 'salary', 'John'
	amount, desc = 100, 'rent'
	test_input = _type_in_deposit_command(name, amount, desc) + \
				 _type_in_withdraw_command('', amount, desc) + 'exit'
	process = _run_cli(test_input)
	assert process.returncode == 0
	assert 'Unsuccessful operation: Client name must not be empty' in process.stdout


def test_withdraw_wont_be_created_if_amount_is_not_provided():
	"""Тест проверяет, что операция списания денег не будет создана, если не указана сумма."""
	name, desc = 'John', 'salary'
	test_input = _type_in_withdraw_command(name, 0, desc) + 'exit'
	process = _run_cli(test_input)
	assert process.returncode == 0
	assert 'Unsuccessful operation: Amount must be greater than zero' in process.stdout
	assert 'was successful' not in process.stdout


def test_withdraw_wont_be_created_if_description_is_not_provided():
	"""Тест проверяет, что операция списания денег не будет создана, если не указано описание."""
	name, amount = 'John', 100
	test_input = _type_in_withdraw_command(name, amount, '') + 'exit'
	process = _run_cli(test_input)
	assert process.returncode == 0
	assert 'Unsuccessful operation: Description must not be empty' in process.stdout
	assert 'was successful' not in process.stdout


def test_show_balance_wont_be_created_if_client_name_is_not_provided():
	"""Тест проверяет, что операция просмотра баланса не будет создана без имени клиента"""
	test_input = _type_in_show_balance_command('') + 'exit'
	process = _run_cli(test_input)
	assert process.returncode == 0
	assert 'Unsuccessful operation: Client name must not be empty' in process.stdout


def test_show_balance_without_operations_will_return_no_operations_message():
	"""Тест проверяет, что клиент увидит сообщение о том, что операций нет, если их нет."""
	name = 'John'
	test_input = _type_in_show_balance_command(name) + 'exit'
	process = _run_cli(test_input)
	assert process.returncode == 0
	assert 'No operations found.' in process.stdout


def test_show_balance_with_incorrect_since_and_till_arguments_will_return_error_message():
	"""Тест проверяет, что если указать since больше till, вызовется исключение."""
	name = 'John'
	test_input = _type_in_show_balance_command(name,
											   since="2019-01-01 00:00:00",
											   till="2018-01-31 00:00:00") + 'exit'
	process = _run_cli(test_input)
	assert process.returncode == 0
	assert 'Unsuccessful operation: Start date must be less than end date' in process.stdout


def test_show_balance_wont_show_operations_beyond_the_specified_period():
	"""Тест проверяет, что операции за пределами указанных промежутков не будут показаны."""
	name = 'John'
	test_input = _type_in_deposit_command(name, 100, 'salary') + \
				 _type_in_withdraw_command(name, 50, 'rent') + \
				 _type_in_show_balance_command(name,
											   since="2019-01-01 00:00:00",
											   till="2020-01-31 00:00:00") + 'exit'
	process = _run_cli(test_input)
	assert process.returncode == 0
	assert 'No operations found.' in process.stdout


def _run_cli(data_input: str) -> subprocess.CompletedProcess:
	"""Запускает программу и возвращает результат ее работы."""
	return subprocess.run(args=['python', ENTRY_POINT], encoding='utf-8',
						  stdout=subprocess.PIPE, input=data_input)


def _type_in_deposit_command(client_name: str, amount: float, description: str) -> str:
	"""Возвращает команду для внесения денег на счет."""
	return f'deposit --client "{client_name}" --amount {amount} ' \
		   f'--description "{description}"' + '\n'


def _type_in_withdraw_command(client_name: str, amount: float, description: str) -> str:
	"""Возвращает команду для списания денег со счета."""
	return f'withdraw --client "{client_name}" --amount {amount} ' \
		   f'--description "{description}"\n'


def _type_in_show_balance_command(client_name: str, since: Optional[str] = None,
								  till: Optional[str] = None) -> str:
	"""Возвращает команду для показа баланса пользователя."""
	return f'show_bank_statement --client "{client_name}" --since "{since}" --till "{till}"\n'