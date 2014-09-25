import unittest

from netViz.deprec.getInput import *

class input_check(unittest.TestCase):
    def test_add_and_check_researched_nodes(self):


print ' === check() === '
# no in
print '""=>'+check('')
print '"\\t"=>'+check('\t')
print '"\\n"=>'+check('\n')

# single word
print '"apple"=>'+check('apple')
print '"grape."=>'+check('grape.')
print '"orange?"=>'+check('orange?')
print '"banana!"=>'+check('banana!')

# sentences
print '"strawberry, sucka."=>'+check('strawberry, sucka.')
print '"is this kiwi?"=>'+check('is this kiwi?')

# multiple sentences
print '"gimmie dat melon. Thank you kindly."=>'+check('you gimmie dat melon? (you hand me "dat melon") Splendid! Thank you kindly.')

print '\n === prompt() === '
test = prompt()
print 'your input is "' + test + '"'
