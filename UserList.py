import random

usersInPool = []


def addUser(name):
    if name is None:
        return False
    if name in usersInPool:
        return False
    else:
        usersInPool.append(name)
        return True


def getUserList():
    return usersInPool


def deleteUser(name):
    usersInPool.remove(name)


def userCount():
    return len(usersInPool)


def resetUsers():
    usersInPool.clear()


def getWinner():
    numUsers = len(usersInPool)
    if numUsers > 1:
        o = random.randrange(1, numUsers)
    elif numUsers == 1:
        o = 0
    else:
        return None
    return usersInPool[o]

