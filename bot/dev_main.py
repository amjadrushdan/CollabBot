import logging
import meta

meta.logger.setLevel(logging.DEBUG)
logging.getLogger("discord").setLevel(logging.INFO)
logging.getLogger('matplotlib.font_manager').disabled = True

from utils import interactive  # noqa

import main  # noqa
