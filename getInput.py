
def prompt():
    print 'waiting for input...'
    uIn = raw_input()    # userInput

    if check(uIn) == 'ERR':
        return prompt()
    else:
        return check(uIn)

def check(uIn):
    if(len(uIn) < 1):
        print 'input length must be > 1'
        return 'ERR'


    if(uIn[-1] == '?'):
        return 'question'
    elif(uIn[-1] == '.'):
        return 'statement'
    else:
        print 'input must end with "." or "?"'
        return 'ERR'
