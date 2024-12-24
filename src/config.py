import os

import dotenv


PATH = os.path.join(os.pardir, ".env")

CONFIG = dotenv.dotenv_values(PATH)
