import logging.config
from time import sleep

import fire

from core.commands import Commands
from core.exceptions import ProgramExit
from core import settings
from core import utils


logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    while True:
        query = utils.get_query()
        try:
            fire.Fire(Commands, query)
        except ProgramExit:
            break
        except BaseException as e:
            sleep(.2)
            logger.error(e)
            print('Unsuccessful operation.')
