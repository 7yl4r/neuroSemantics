__author__ = 'tylar'

import math

INIT_VAL = 100  # starting value for a new connection
DEGRADER = 50  # controls amount connections degrade over time
STRENGTHENER = 50  # controls amount connections strengthe n with use


class Connection(object):
    def __init__(self):
        self.value = INIT_VAL

    def __add__(self, other):
        return self.value + other

    def __sub__(self, other):
        return self.value - other

    def strengthen(self):
        """
        increases strength of connection.
        inverse log function is used to give boost to new weaker connections over existing strong ones.
        """
        self.value += 1+1000/int(math.log(self.value))

    def degrade(self):
        """
        decreases strength of connection as if weakend by non-use
        :return:
        """
        self.value -= DEGRADE