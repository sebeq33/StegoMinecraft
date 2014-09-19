import sys

class Ref(object): ##"object" needed for @val.setter (new-style classes)
    def __init__(self, value = None):
        if (value == None):
            self._x = None
        else:
            self._x = [value]

    def Set(self, value):
        self._x = [value]

    def Get(self):
        if self._x == None:
            return None
        return (self._x[0])

    def Unset(self):
        if self._x != None:
            del self._x[0]
            self._x = None
    
    @property
    def val(self):
        return self.Get()

    @val.setter
    def val(self, value):
        self.Set(value)

    @val.deleter
    def val(self):
        self.Unset()

## ================= INCR ===================

def incr(i):
    i.Set(i.Get() + 1)

def incr2(i):
    i += 1

## ================= TEST 1 ===================

def test1():
    ref = Ref()
    print (ref.Get() == None)   # True
    ref.Set(42)
    print (ref.Get() == 42)     # True
    ref.Set(55)
    print (ref.Get() == 55)     # True
    ref.Unset()
    print (ref.Get() == None)   # True

## ================= TEST 2 ===================

def test2():
    ref = Ref()
    ref.val = "Hello"
    print (ref.Get() == "Hello")
    ref.val += " World !"
    print (ref.Get() == "Hello World !")

## ================= TEST 3 ===================

def test3():
    ref = Ref(55)

    incr(ref)           ## passing ref, containing mutable dict, so +1
    print (ref.val == ref.Get() and ref.val == 56)
    incr2(ref.val)      ## new val is a copy, so no +1
    print (ref.val == ref.Get() and ref.val == 56)

    ref.val += 1        ## use @property and @val.setter as getter/setter combo, like incr(ref)
    print (ref.val == ref.Get() and ref.val == 57)
    ref.val += 1
    print (ref.val == ref.Get() and ref.val == 58)

## ================= MAIN ===================

def main(argv):
    # test1()
    # print "---------------------------------------"
    test2()
    print "---------------------------------------"
    test3()

if __name__ == '__main__':
    print "---------------------------------------"
    print "---------------------------------------"
    sys.exit(main(sys.argv))
