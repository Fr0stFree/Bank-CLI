import logging
import logging.config
import sys

import fire

from core import settings
from core.commands import Commands
from core.utils import HELLO_MESSAGE, BYE_MESSAGE

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)


def get_query() -> str:
	"""Получение запроса от пользователя."""
	try:
		return input('>>> ')
	except KeyboardInterrupt:
		print(BYE_MESSAGE)
		sys.exit(0)


if __name__ == '__main__':
	print(HELLO_MESSAGE)
	commands = Commands()
	while True:
		query = get_query()
		fire.Fire(commands, query)
