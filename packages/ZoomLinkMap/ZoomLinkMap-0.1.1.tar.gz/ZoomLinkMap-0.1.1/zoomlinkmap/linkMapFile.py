
class LinkMapFile:
    arch = None
    files = {}
    path = None
    def __init__(self):
        pass
    def cacheObjFile(self, file, hashKey):
        self.files[str(hashKey)] = file
        pass
    def objFileCached(self, hashKey):
        if self.files.has_key(str(hashKey)):
            return self.files[str(hashKey)]
        else:
            return None
        pass
    pass

class ObjFile:
    haskKey = None
    path = None
    name = None
    functions = {}
    size = 0
    moduleName = None
    def __init__(self):
        self.size =0
        pass
    def appendFunction(self, func):
        if self.functions.has_key(func.address) == False:
            self.functions[func.address] = func
            self.size += func.size
        else:
            print "get key"
    pass

class ObjInfoRecord:
    def __init__(self, owner, info, address ,size):
        self.size = int(size, 16)
        self.address = address
        self.owner = owner
        self.info = info

        pass
    pass
class UnknownRecord(ObjInfoRecord):
    pass
class InstanceFunction(ObjInfoRecord):
    fileName = None
    funcName = None
    pass

class ClassFunction(InstanceFunction):
    pass

def ObjInfoRecordFactory(owner, info ,address, size):
    if info.startswith("+["):
        func = ClassFunction(owner, info, address, size)
        info = info[2:-1]
        parts = info.split(' ')
        if len(parts) == 2:
            func.fileName = parts[0]
            func.funcName = parts[1]
            pass
        return func
        pass
    elif info.startswith("-["):
        func = InstanceFunction(owner, info, address, size)
        info = info[2:-1]
        parts = info.split(' ')
        if len(parts) == 2:
            func.fileName = parts[0]
            func.funcName = parts[1]
            pass
        return func
        pass
    else:
        func = UnknownRecord(owner, info, address, size)
        return func
    pass
