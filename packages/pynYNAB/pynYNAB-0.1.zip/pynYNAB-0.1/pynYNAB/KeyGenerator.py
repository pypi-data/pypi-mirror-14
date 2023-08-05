import uuid

def generateuuid():
    return str(uuid.uuid4())

def deterministicuuid(inputobject):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS,str(inputobject)))
