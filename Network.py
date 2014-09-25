from Connection import Connection

# TODO: add MAX_CONNECTIONS, preallocate connections dict, and then overwrite weakest when learning

ACTIVATION_THRESH = 9000  # activation threshold which triggers outgoing connections for a node

ACTIVATION_VALUE = 10000  # value which a node is given when activated

RESP_MAX_LEN = 50  # max number of semantic concepts (words) network yields in responses
RESP_THRESH = 1000  # activation threshold which nodes must be above to be included in response

DESIRED_MEAN = ACTIVATION_THRESH/3
DESIRED_VARIANCE = ACTIVATION_THRESH/2


class NetworkState(object):
    """
    defines the state of the network, ie: the activation levels of all the nodes
    """
    def __init__(self):
        self.nodes = dict()

    def activate_nodes(self, stmt):
        """
        activates nodes in given stmt
        """
        for word in stmt:
            self.activate_node(word)

    def activate_node(self, word):
        self.nodes[word] = ACTIVATION_VALUE
        # TODO: does the previous value of the node matter??? What about recovery time?
        # TODO: what if the node has no connections? is that possible here?

    def get_statement(self):
        """
        reads the state and outputs a statement based on the most highly activated nodes
        """
        # TODO: sort and use the max (first or last) in node dict for better performance?
        resp = list()
        for word in self.nodes:
            if self.nodes[word] > RESP_THRESH:
                resp.append(word)
                if len(resp) > RESP_MAX_LEN:
                    return resp
        return resp


class Network(object):
    """
    encapsulates all information on the network of nodes including association information and state information
    """
    def __init__(self):
        self.connections = dict()
        self.state = NetworkState()

    def get_connection_strength_mean(self):
        """
        :return: the mean of all connection values for dynamic param shifting
        """
        return sum(self.nodes.values())/float(len(self.nodes))

    def get_connection_strength_variance(self):
        """
        :return: the variance of all connection values for dynamic param shifting
        """
        return max(self.nodes.values()) - min(self.nodes.values())

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
        print self.state.get_statement()

    def run(self, think_time=5):
        """
        interates over the entire network, propagating signals between nodes
        :param think_time: number of cycles to run the state
        """
        self.balance_params()
        # propagate via connections
        for conn in self.connections:
            w1, w2 = unformat_connection_key(conn)
            connect = self.connections[conn]
            stren = connect.value
            if self.state.nodes[w1] > ACTIVATION_THRESH:
                # send signal forward to next connection based on strength
                self.state.nodes[w2] = stren + self.state.nodes[w2]

                # strengthen used connections
                connect.strengthen()

            # degrade all connections over time
            connect.degrade()

    def balance_params(self):
        """
        balances parameters guiding strength increase/decreases in an attempt to achieve the
        desired distribution.
        :return:
        """
        mean = self.get_connection_strength_mean()
        if mean < DESIRED_MEAN:
            # boost strengthener
            NotImplementedError()
        elif mean > DESIRED_MEAN:
            # boost degradation
            NotImplementedError()

        var = self.get_connection_strength_variance()
        if var < DESIRED_VARIANCE:
            # boost strengthening and degradation?
            NotImplementedError()
        # variance can't be too high?

        print 'm:', mean, '\tv:', var

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