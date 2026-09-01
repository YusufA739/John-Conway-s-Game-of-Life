import copy, random
from copy import deepcopy


def shiftFrameToBeginning(listQueue, queueLength=None, newLastElement=None):
    # deque and enqueue
    queueLength = len(listQueue) if queueLength is None else queueLength  # autofilled code, need to research this
    for carrier in range(0, queueLength - 1, 1):
        # update all unaltered lines down, skipping overwriting the first, so line 1 and 2 will be identical for now,
        # and also not rewriting the last line to another line
        listQueue[carrier] = deepCopy(listQueue[carrier + 1])

    # listQueue[0] = newFinalElement.copy() if newFinalElement is not None else listQueue[0].copy()
    if newLastElement is not None:
        listQueue[queueLength - 1] = deepCopy(newLastElement)

    return (listQueue)

def deepCopy(list1):
    return copy.deepcopy(list1)

list1 = [1,2,3,4,5,6,7,8,9,10]

for carrier in range(len(list1)):
    list1 = deepcopy(shiftFrameToBeginning(list1, newLastElement=random.randint(0,9)))
    print(list1)