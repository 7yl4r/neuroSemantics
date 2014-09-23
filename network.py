class network:

    def getNode(self, nodeName):
        print 'looking for node "'+nodeName+'"...'
        return 'not found'

    def increaseConnection(self,n1,n2,upVal):
        # check for self-connection
        if (n1 == n2):
            return
        # implied else:
        print n1+'->'+n2+'+='+str(upVal)
        return

    def insertNode(self,nodeName):
        print 'inserting node "'+nodeName+'"...'
        return
