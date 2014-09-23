import string

def trainOnStatement(network, stmt):
    nodes = string.split(stmt) # make list of statement semantics

    # add non-existing semantic nodes
    for n in nodes:
        if network.getNode(n) == 'not found':
            network.insertNode(n)

    # increase connection strength between all nodes in statement
    upVal = .1
    for n1 in nodes:
        for n2 in nodes:
            network.increaseConnection(n1,n2,upVal)

