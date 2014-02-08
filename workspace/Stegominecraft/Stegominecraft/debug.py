
#print all disponible methods for one given object
def printMethods(obj):
    for m in [m for m in dir(obj) if callable(getattr(obj, m))]:
        print m

def printObject(obj):
    for m in dir(obj):
        print m
