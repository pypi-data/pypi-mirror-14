from . import cli
import sys

class FakeOut:
    def __init__(self):
        self.str=''
        self.n=0
    def write(self,s):
        self.str += s
        self.n+=1
    def result(self):
        return self.str
    def clear(self):
        self.str=''
        self.n=0

def cmd(argv):
    f = FakeOut()
    old = sys.stdout
    sys.stdout = f
    cli.program.parse(argv)
    sys.stdout = old
    return f.result()