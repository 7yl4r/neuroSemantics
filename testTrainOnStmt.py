import network
from trainOnStatement import *
import vizHandler

stmt = 'sky is blue'
net = network.network()

trainOnStatement(net,stmt)

v = vizHandler.viz()
v.showNet()
