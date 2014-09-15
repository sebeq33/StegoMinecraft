import sys

class Ref():
    def __init__(self, value = None):
        if (value == None):
            self._value = None
        else:
            self._value = [value]

    def Set(self, value):
        self._value = [value]

    def Get(self):
        if self._value == None:
            return None
        return (self._value[0])

    def Unset(self):
        self._value = None

def main(argv):
    ref = Ref()
    print ref
    print ref.Get()
    ref.Set(42)
    print (ref.Get())
    ref.Set(55)
    print ref.Get()
    ref.Unset()
    print ref
    print ref.Get()
    
if __name__ == '__main__':
    print "---------------------------------------"
    print "---------------------------------------"
    sys.exit(main(sys.argv))
