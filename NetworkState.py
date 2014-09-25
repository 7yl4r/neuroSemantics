__author__ = '7yl4r'

from PIL import Image
import pylab

RESP_MAX_LEN = 50  # max number of semantic concepts (words) network yields in responses
RESP_THRESH = 1000  # activation threshold which nodes must be above to be included in response

ACTIVATION_VALUE = 10000  # value which a node is given when activated


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

    def plot_img(self, save_file_loc):
        """
        puts all values in the state into an image & saves to given file
        """
        cmap = pylab.cm.get_cmap(name='spectral')
        size = len(self.nodes) / 2 + 1

        rng, mini, maxi = self.get_range()

        img = Image.new('RGB', (size, size), "black")  # create a new black image
        pixels = img.load()  # create the pixel map
        valus = self.nodes.values()
        for i in range(img.size[0]):    # for every pixel:
            for j in range(img.size[1]):
                try:
                    colour = cmap((valus[i + j] - mini) / (maxi - mini))
                    colour = (int(colour[0] * 255), int(colour[1] * 255), int(colour[2] * 255))
                    print colour
                    pixels[i, j] = colour  # set the colour accordingly
                except IndexError:
                    continue

        img.save(save_file_loc)

    def get_range(self):
        """
        :return: the variance of all connection values for dynamic param shifting
        """
        maxi = max(self.nodes.values())
        mini = min(self.nodes.values())
        return int(maxi - mini), maxi, mini