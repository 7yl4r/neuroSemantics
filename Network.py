from Connection import Connection
from NetworkState import NetworkState

import glob
import os

# TODO: add MAX_CONNECTIONS, preallocate connections dict, and then overwrite weakest when learning

ACTIVATION_THRESH = 9000  # activation threshold which triggers outgoing connections for a node

DESIRED_MEAN = ACTIVATION_THRESH/3
DESIRED_RANGE = ACTIVATION_THRESH/2


class Network(object):
    """
    encapsulates all information on the network of nodes including association information and state information
    """
    def __init__(self):
        self.connections = dict()
        self.state = NetworkState()
        self.input_count = 0

        # clear out any old state images
        for f in glob.glob('./states/s*'):
            os.remove(f)

    def get_connection_strength_mean(self):
        """
        :return: the mean of all connection values for dynamic param shifting
        """
        return int(sum(self.connections.values())) / float(len(self.connections))

    def get_connection_strength_range(self):
        """
        :return: the variance of all connection values for dynamic param shifting
        """
        maxi = max(self.connections.values()).value
        mini = min(self.connections.values()).value
        return int(maxi - mini), maxi, mini

    def learn_statement(self, stmt):
        """
        network learns given statement
        :param stmt:
        :return:
        """
        for word1 in stmt:
            for word2 in stmt:
                if word1 == word2:
                    continue
                else:
                    self.associate(word1, word2)
            self.state.activate_node(word1)

    def respond_to_question(self, qtn):
        """
        network yields response to inquiry
        :param qtn:
        :return:
        """
        # input the question into the network by activating the nodes
        self.state.activate_nodes(qtn)

        # run a few cycles
        self.run()

        # read the network state
        for node in self.state.nodes:
            print node, '\t:', self.state.nodes[node]

        print self.state.get_statement()

    def run(self, think_time=20):
        """
        interates over the entire network, propagating signals between nodes
        :param think_time: number of cycles to run the state
        """
        self.redist()
        # propagate via connections
        for conn in self.connections:
            w1, w2 = unformat_connection_key(conn)
            connect = self.connections[conn]
            stren = connect.value
            if self.state.nodes[w1] > ACTIVATION_THRESH:
                # send signal forward to next connection based on strength
                self.state.input_to_node(w2, stren)

                # strengthen used connections
                connect.strengthen()

            # degrade all connections over time
            connect.degrade()

    def balance_params(self, verbose=True):
        """
        balances parameters guiding strength increase/decreases in an attempt to achieve the
        desired distribution.
        :return:
        """
        mean = self.get_connection_strength_mean()
        if mean < DESIRED_MEAN:
            # boost strengthener
            raise NotImplementedError()
        elif mean > DESIRED_MEAN:
            # boost degradation
            raise NotImplementedError()

        rng = self.get_connection_strength_range()
        if rng < DESIRED_RANGE:
            # boost strengthening and degradation?
            raise NotImplementedError()
        # rng can't be too high?

        if verbose:
            print 'conn stren m:', mean, '\tv:', rng

    def redist(self, verbose=True):
        """
        redistributes connection strengths to match desired distribution.
        """
        mean = self.get_connection_strength_mean()
        # move all values to the mean
        shift = DESIRED_MEAN - mean
        #print self.connections
        for conn in self.connections.values():
            #print conn
            conn.value += shift

        rng, maxi, mini = self.get_connection_strength_range()
        scale = 0
        if rng <= 0:
            print 'WARN: range <= 0'
        elif rng < DESIRED_RANGE:
            newMax = mean + DESIRED_RANGE / 2
            newMin = mean - DESIRED_RANGE / 2
            scale = (newMax - newMin) / (maxi - mini)
            for conn in self.connections:
                self.connections[conn].value = (self.connections[conn].value - mini) * scale + newMin
        # rng can't be too high?

        if verbose:
            print 'conn stren m:', mean, '\tv:', rng
            print 'adjustment m:', shift, '\tv:', scale

    def associate(self, w1, w2):
        """
        associates two words with each other (increases connection between semantic nodes)
        :param w1:
        :param w2:
        :return:
        """
        try:
            self.connections[format_connection_key(w1, w2)].strengthen()
        except KeyError:
            self.connections[format_connection_key(w1, w1)] = Connection()

    def plot_state_file(self):
        """
        prints the next state file to appropriately numbered image.
        """
        self.state.plot_img('./states/s' + str(self.input_count) + '.jpg')
        self.input_count += 1

    def input_file(self, file_name):
        """
        Uses txt file as input. Tokenizes by line. Assumes each line ends with period ('.');
         no other punctuation should be included.
        """
        lines = [line.rstrip('\n') for line in open(file_name)]
        for line in lines:
            lin = format_line(line)
            self.learn_statement(lin)
            self.run()
            self.plot_state_file()

    #################################################
    ### OLD HALF-IMPLEMENTED FUNCTIONS BELOW HERE ###
    #################################################
    def get_node(self, nodeName):
        print 'looking for node "'+nodeName+'"...'
        raise NotImplementedError()
        return 'not found'

    def increase_connection(self,n1,n2,upVal):
        # check for self-connection
        if n1 == n2:
            return
        # implied else:
        print n1+'->'+n2+'+='+str(upVal)
        raise NotImplementedError()
        return

    def insert_node(self, nodeName):
        print 'inserting node "'+nodeName+'"...'
        raise NotImplementedError()
        return


def unformat_connection_key(key):
    """
    returns words from formatted connection key
    :param key: the key to unformat
    :return: [word1, word2]
    """
    return key.split('|')

def format_connection_key(w1, w2):
    """
    returns a formatted string to be used in the connections dict
    :param w1:
    :param w2:
    :param strength:
    :return:
    """
    return str(w1)+'|'+str(w2)

def format_line(line):
    """
    changes a sentence into a properly formatted list
    """
    line = line.replace('?', '')
    line = line.replace('.', '')
    return line.split(' ')