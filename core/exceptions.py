class NotEnoughMoneyError(Exception):
	"""Raised when the user does not have enough money to withdraw."""
	pass

class ProgramExit(SystemExit):
	"""Raised when the user wants to exit the program."""
	pass