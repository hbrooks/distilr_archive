from datetime import datetime
import json

import numpy as np


class DistilrJsonSerializer:

    @staticmethod
    def dt_to_string(dt):
        return str(int(dt.timestamp()))

    @staticmethod
    def string_to_dt(string):
        return datetime.fromtimestamp(int(string))
