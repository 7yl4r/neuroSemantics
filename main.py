__author__ = 'tylar'

from Network import Network

EXITS = ['exit', 'quit']


class STMT_TYPES(object):
    question = 1
    statement = 2
    ERR = -1


def prompt():
    print 'waiting for input...'
    uIn = raw_input()    # userInput
    typ = check(uIn)
    if typ == STMT_TYPES.ERR:
        return prompt()
    else:
        uIn = uIn.replace('?', '')
        uIn = uIn.replace('.', '')
        return typ, uIn.split(' ')


def check(uIn):
    if len(uIn) < 1:
        print 'input length must be > 1'
        return 'ERR'
    elif uIn in EXITS:
        exit()
    elif uIn[-1] == '?':
        return STMT_TYPES.question
    elif uIn[-1] == '.':
        return STMT_TYPES.statement
    else:
        print 'input must end with "." or "?"'
        return STMT_TYPES.ERR


network = Network()

while True:
    typ, inp = prompt()
    if typ == STMT_TYPES.statement:
        network.learn_statement(inp)
    elif typ == STMT_TYPES.question:
        network.respond_to_question(inp)

    # give the net some alone time to think... (and recover from i/o barrage)
    network.run()
    network.state.plot_img('./net_state.jpg')