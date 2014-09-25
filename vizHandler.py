from subprocess import Popen


class viz:
#    def __init__(self):
        # set up the file server for d3 visuals
        #self.server = Popen("python -m SimpleHTTPServer", shell=True)
        #print 'python server started @ pid '+str(self.server.pid)

    def showNet(self):
        print 'WARNING: this is experimental. please make sure you have an http server set up before use. This can be set up by running "python -m SimpleHTTPServer" from the package base directory. Continue? y/n'
        uIn = raw_input()
        if uIn == 'n':
            return
        elif uIn == 'y':
            self.v1 = Popen("x-www-browser http://localhost:8000/netViz/forceDirected.html",shell=True)
            print 'viz opened in your browser @ pid '+str(self.v1.pid) + 'press enter to continue'
            raw_input()
            return
        else:
            self.showNet()

    def __del__(self):
        self.v1.kill()

# none of these seem to work:
    #    kill(self.server.pid)
    #    self.server.terminate()
    #    self.server.kill()

