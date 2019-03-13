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
    if(arr[4] == "d"):
        DFS(arr)
    elif(arr[4] == "g"):
        greedy(arr)
    elif(arr[4] == "a"):
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
    print("tiebreaker function\n")

### Function to check tree for already seen values. ###
def checkTreeForDups(tree, stack):

    ## If a success add to tree to become noticable, duplicate winners are fine and expected ## 
    if(checkSuccess(stack)):
        return False
    
    ## Array of nodes will be a test array to see if it exists ## 
    arrayOfNodes = anytree.find(tree, lambda nodes: nodes.name == stack)
    if(arrayOfNodes > 0):
        return True
    else:
        return False

### Creating the tree used for algorithms ###
def createTree(arr):

    ## Parent Node ##
    ROOT = Node(arr)

    ## Makes the first 3 leaf nodes for parent then begins recursion ## 
    for x in range(3):
        tmp = arr[:]
        flip(tmp, x + 2)
        tmpNode = Node(tmp, parent=ROOT)
        makeLeaves(tmp, tmpNode, ROOT)
        global recursionVAR
        recursionVAR = 0

    ## Print Tree for viewing purposes ##
    print(RenderTree(ROOT))

### Recursive function to make leaves ###
def makeLeaves(arr, node, rootNode):
    ROOT = rootNode
    global recursionVAR
    recursionVAR = recursionVAR + 1

    ## If what we are looking at is a success dont continue ## 
    if(checkSuccess(arr) != True):
        for x in range(3):
            tmp = arr[:]
            flip(tmp, x+1)

            ## Check for duplicates before continuing ##
            if(checkTreeForDups(ROOT, tmp) == False):
                tmpNode = Node(tmp, parent=node)

                ## Set recursion value, used for testing will change when bigger trees are required ## 
                if(recursionVAR < 3):
                    makeLeaves(tmp, tmpNode, rootNode)
    else:
        ## Testing Print ## 
        print("WINNER WINNER")
    

### DFS Algorithm. ###
def DFS(arr):
    print("dfs")
    

### A* Algorithm. ###
def aStar(arr):
    print("a*")

### Greedy Algorithm. ###
def greedy(arr):
    print("greedy")

### UCS Algorithm. ###
def UCS(arr):
    print("UCS")



### Main function, user input and function calls. ###
def main():
    stack = raw_input("Gimme a pancake\n")
    stack = list(stack)

    ### Check initial list ###
    checkList(stack)

    ### Create the tree ###
    createTree(stack)

    runAlgorithm(stack)
    
### Python stuff ya know. ###
if __name__ == "__main__":
    main()