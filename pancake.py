import os
import sys
import anytree
from anytree import Node, RenderTree

recursionVAR = 0
arr = []
ROOT = Node(arr)

### Checking given array to make sure it is correct format. ###
def checkList(arr):
    if(len(arr) != 5):
        print("Incorrect format")
        main()
    elif(arr[4] != "d" and arr[4] != "g" and arr[4] != "a" and arr[4] != "u"):
        print("Not a correct search algorithm")
        main()

### Running desiered algorithm based off last char. ###
def runAlgorithm(arr):
    if(arr.name[4] == "d"):
        DFS(arr)
    elif(arr.name[4] == "g"):
        greedy(arr)
    elif(arr.name[4] == "a"):
        aStar(arr)
    else:
        UCS(arr)

### Used to check if pancake is in sucessful format '4321'. ###
def checkSuccess(arr):
    if(arr[0] == "4" and arr[1] == "3" and arr[2] == "2" and arr[3] == "1"):
        return True
    else:
        return False

### Flip pancakes at i location. ###
def flip(arr, i):
    arr2 = arr[:]

    ## Flipy Flip ## 
    arr2[0] = arr[3]
    arr2[1] = arr[2]
    arr2[2] = arr[1]
    arr2[3] = arr[0]
    start = 0
    while start < i : 
        temp = arr2[start] 
        arr2[start] = arr2[i - 1] 
        arr2[i - 1] = temp 
        start += 1
        i -= 1

    ## Flip Flippy ## 
    arr[0] = arr2[3]
    arr[1] = arr2[2]
    arr[2] = arr2[1]
    arr[3] = arr2[0]

### Check which number is larger to determine next move. ###
def tieBreaker(arr1, arr2):
    for i in range(4):
        if(int(arr1.name[i]) > int(arr2.name[i])):
            return arr1
        elif(int(arr1.name[i]) < int(arr2.name[i])):
            return arr2


### Function to check tree for already seen values. ###
def checkTreeForDups(tree, stack):

    ## If a success add to tree to become noticable, duplicate winners are fine and expected ## 
    if(checkSuccess(stack)):
        return False

    ## Array of nodes will be a test array to see if it exists ## 
    try:
        arrayOfNodes = anytree.find(tree, lambda nodes: nodes.name == stack)
    except: 
        return True
    
    if(arrayOfNodes > 0):
        return True
    else:
        return False

### Creating the tree used for algorithms ###
def createTree(arr):

    ## Parent Node ##
    ROOT = Node(arr, g=0)

    ## Makes the first 3 leaf nodes for parent then begins recursion ## 
    for x in range(3):
        tmp = arr[:]
        flip(tmp, x + 2)
        tmpNode = Node(tmp, parent=ROOT, g=x+2)
        makeLeaves(tmp, tmpNode, ROOT, 0)
        global recursionVAR
        recursionVAR = 0

    ## Print Tree for viewing purposes ##

    '''for pre, _, node in RenderTree(ROOT):
        print("%s%s" % (pre, node.name))

    print("\n ######################## GRAPH #############################")'''

    return ROOT

### Recursive function to make leaves ###
def makeLeaves(arr, node, rootNode, iterator):
    ROOT = rootNode
    global recursionVAR
    recursionVAR = recursionVAR + 1

    ## If what we are looking at is a success dont continue ## 
    if(checkSuccess(arr) != True):
        for x in range(4):
            tmp = arr[:]
            flip(tmp, x+1)
            ## Check for duplicates before continuing ##
            if(tmp != arr):
                value = node.g
                tmpNode = Node(tmp, parent=node, g=(x+1) + value)
                ## Set recursion value, used for testing will change when bigger trees are required ## 
                if(iterator < 6):
                    iterator = iterator + 1
                    makeLeaves(tmp, tmpNode, rootNode, iterator)
    

def printProcess(arr, i, g, h):
    output = ""
    for x in range(4):
        if(x == i):
            output+="|"
            output+=str(arr[x])
        else:
            output+=str(arr[x])
    print(output + "  g=" + str(g) + ", h=" + str(h))

def findDifference(parent, child):
    for i in range(4):
        if(parent[i] != child[i]):
            return i

def findGValue(num):
    if(num == 0):
        return 4
    elif(num == 1):
        return 3
    elif(num == 2):
        return 2
    else:
        return 1

##### Implementing Fringe #####

### Using anytree API I will find all goal nodes created in the graph. ###
def findAllGoalNodes(tree, typeSearch):

    goalNodes = anytree.findall(tree, filter_=lambda node: node.name == ["4", "3", "2", "1", typeSearch])
    return goalNodes

def searchForLowestCost(nodes):
    lowestCost = 100
    tmp = nodes[0]
    for goal in nodes:
        if goal.g < lowestCost:
            lowestCost = goal.g
            tmp = goal
    
    return tmp
        

### DFS Algorithm. ###
def DFS(arr):
    goalNode = arr
    gValue = 0
    ## Run DFS until goal node is found. ##    
    while(checkSuccess(goalNode.name) == False):
        children = goalNode.children
        totalChildren = len(children)
        ## If only one child print and continue. ##
        if(totalChildren == 1):
            num = findDifference(goalNode.name, children.name)
            numValue = findGValue(num)
            gValue = numValue + gValue
            printProcess(goalNode.name, num, gValue, "DNE")
            goalNode = children
        ## For two or more children run a tie breaker and print result. ##
        elif(totalChildren == 2):
            originalNode = goalNode
            goalNode = tieBreaker(children[0], children[1])
            num = findDifference(originalNode.name, goalNode.name)
            numValue = findGValue(num)
            gValue = numValue + gValue
            printProcess(originalNode.name, num, gValue, "DNE")
        elif(totalChildren == 3):
            originalNode = goalNode
            tmp = tieBreaker(children[0], children[1])
            goalNode = tieBreaker(tmp, children[2])
            num = findDifference(originalNode.name, goalNode.name)
            numValue = findGValue(num)
            gValue = numValue + gValue
            printProcess(originalNode.name, num, gValue, "DNE")

    ## Printing final process node ##
    printProcess(goalNode.name, 10, gValue, "DNE")
    

### A* Algorithm. ###
def aStar(arr):
    print("a*")

### Greedy Algorithm. ###
def greedy(arr):
    print("greedy")

### UCS Algorithm. ###
def UCS(arr):
    nodes = findAllGoalNodes(arr, "u")
    UCSNode = searchForLowestCost(nodes)
    
    node = UCSNode.root

    for i in range(len(UCSNode.path)):
        node = UCSNode.path[i]
        
        if(checkSuccess(node.name) != True):
            num = findDifference(node.name, UCSNode.path[i + 1].name)
            printProcess(node.name, num, node.g, "DNE")
        else:
            printProcess(node.name, 10, node.g, "DNE")
        
        
        
    

### Main function, user input and function calls. ###
def main():
    stack = raw_input("Gimme a pancake\n")
    stack = list(stack)

    ### Check initial list ###
    checkList(stack)

    ### Create the tree ###
    ROOT = createTree(stack)
    
    ### Run algorithm as determined by user ###
    runAlgorithm(ROOT)
    
### Python stuff ya know. ###
if __name__ == "__main__":
    main()