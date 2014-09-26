__author__ = 'tylar'

import math

INIT_VAL = 100  # starting value for a new connection
DEGRADER = 25  # controls amount connections degrade over time
STRENGTHENER = 50  # controls amount connections strengthen with use


class Connection(object):
    def __init__(self):
        self.value = INIT_VAL

    def __add__(self, other):
        self.value += int(other)
        return self

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        self.value -= int(other)
        return self

    def __rsub__(self, other):
        self.value = int(other) - self.value
        return self

    def __int__(self):
        return int(self.value)

    def strengthen(self):
        """
        increases strength of connection.
        inverse log function is used to give boost to new weaker connections over existing strong ones.
        """
        #print 'val:', self.value
        if self.value < 1:
            self.value = INIT_VAL
            print 'WARN: temporary conn stren val < 1 hack used.'
        else:
            self.value += 1 + 1000 / int(math.log(self.value))

    def degrade(self):
        """
        decreases strength of connection as if weakend by non-use
        :return:
        """
        self.value -= DEGRADER
        if self.value < 1:
            print 'WARN: conn completely degraded. TODO: del'
            # TODO: remove conn
            self.value = 1
