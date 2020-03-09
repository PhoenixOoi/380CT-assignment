import itertools
import random
import time
import copy

#----------------------------------------------------------------------------
#       GENERATE ARRAY
#----------------------------------------------------------------------------
def randomSet():
    #initialize the array
    set = []

    #set length of array
    length = 15

    #range of numbers
    numRange = 100
    
    #for loop append randomize numbers into array
    for i in range(length):
        r = random.randint(0, numRange)
        if r not in set: 
            set.append(r)
        else: 
            while r in set:
                r = random.randint(0, numRange)
            set.append(r)
           
    return set


def validateSet(arr):
    #partition = []# partition stores the index where the numbers are added in the partition of the set
    sum = calculateSum(arr)

    #if the sum is divisible by 3, it can be divided into 3 partitions with equal sum
    if (sum%3) == 0 :
        #print("sum: ", sum)
        return True
    else:
        #return false to loop and generate new set of random numbers
        return False


def initializeArr():
    valid = False
    arr = []
    
    #loop until a valid set is obtained
    while valid == False:
        #get random set
        arr = randomSet()
        valid = validateSet(arr)

    #print("set: ", arr)
    return arr


#----------------------------------------------------------------------------
#   GREEDY METHOD
#----------------------------------------------------------------------------

def greedy(arr):
    A = []
    B = []
    C = []

    #sort the numbers
    for i in sorted(arr, reverse = True):
        #put i into the smallest sum partition set
        if calculateSum(A) <= calculateSum(B) and calculateSum(A) <= calculateSum (C):
            A.append(i)
        elif calculateSum(B) < calculateSum(A) and calculateSum(B) <= calculateSum(C):
            B.append(i)
        elif calculateSum(C) < calculateSum(A) and calculateSum(C) < calculateSum(B):
            C.append(i)
       
    return (A, B, C)

#find 2 sets with the largest dfference
def getSwapSet(diffArr, setArr):
    swapSet_1 = -1
    swapSet_2 = -1
    remainSet = -1
    

    maxDiff_1 = 0
    maxDiff_2= 0
    
    
    
    tempArr = [0, 1, 2]

    
    for i in range(len(diffArr)):
        if maxDiff_1 < diffArr[i]:
            maxDiff_2 = maxDiff_1
            maxDiff_1 = diffArr[i]

            swapSet_2 = swapSet_1
            swapSet_1 = i
            
            
        elif maxDiff_2 < diffArr[i]:
            maxDiff_2 = diffArr[i]
            swapSet_2 = i

   
    tempArr.remove(swapSet_1)
    tempArr.remove(swapSet_2)

    remainSet = int(tempArr[0])

    return (swapSet_1, swapSet_2, remainSet)



#----------------------------------------------------------------------------
#   LOCAL SEARCH METHOD
#----------------------------------------------------------------------------

#A, B are the selected sets to be swapped with their elements
#swap the numbers until solution is found, if not, elements are randomly swapped
#to increase probability to find better solution
def localSearch(A, B, thirdSum):
    
    betterA = []
    betterB = []

    
    diffA = abs(thirdSum - calculateSum(A))
    diffB = abs(thirdSum - calculateSum(B))

    
    for h in range(3):

        #on 2nd loop: smallest element in B is added to A
        if h == 1 and abs(thirdSum - calculateSum(A)) != 0:
            minIndex = 0
            for k in range(len(B)):
                if k == 0:
                    min = B[k]
                elif min > B[k]:
                    min = B[k]
                    minIndex=k

            A.append(B[minIndex])
            B.remove(B[minIndex])
            

        #on 3rd loop: 2 smallest elements of A are added to B
        if h == 2:
            for m in range(2):
                minIndex = 0
                for k in range(len(A)):
                    if k == 0:
                        min = A[k]
                    elif min > A[k]:
                            min = A[k]
                            minIndex = k
                
                B.append(A[minIndex])
                A.remove(A[minIndex])

        #swap B elements with A elements one by one to find best solution
        #return when one or both of (A,B) has 0 difference with sum/3(thirdSum)
        #return value: found best A and B, True = solution found, False = solution not found yet
        for i in range(len(A)):
            for j in range(len(B)):
                temp = A[i]    
                A[i] = B[j]
                B[j] = temp

                if thirdSum == calculateSum(A) and thirdSum == calculateSum(B):
                    return A, B, True
                    break

                elif thirdSum == calculateSum(A) or thirdSum == calculateSum(B):
                    return A, B, False
                    break

                elif abs(thirdSum - calculateSum(A)) < diffA or abs(thirdSum - calculateSum(B)) < diffB:
                     
                    betterA = []
                    betterB = []
                    betterA.extend(A)
                    betterB.extend(B)

                    diffA = abs(thirdSum - calculateSum(A))
                    diffB = abs(thirdSum - calculateSum(B))
                    
                else:
                    B[j] = A[i]
                    A[i] = temp

    #return if better solutions are found
    if len(betterA) > 0:
        if betterA is not None:
            return betterA, betterB, False
    else:#if after local search, better solution not found
        #add back 2 smallest elements from B to A
        minIndex = 0
        for k in range(len(B)):
            if k == 0:
                min = B[k]
            elif min > B[k]:
                min = B[k]
                minIndex = k
                       
        A.append(B[minIndex])
        B.remove(B[minIndex])

        #since there is no better solution found, randomly swap between TWO numbers
        #numbersToChange = number of times to swap between two numbers
        numbersToChange = random.randint(0, len(A))

        for i in range (numbersToChange):
            numToAppend = random.randint(0, len(B)-1)#so that it randoms in array index
            numToRemove = random.randint(0, len(A)-1)#so that it randoms in array index

            A.append(B[numToAppend])
            B.remove(B[numToAppend])

            B.append(A[numToRemove])
            A.remove(A[numToRemove])
 
        return A, B, False



#----------------------------------------------------------------------------
#   SUPPORTING METHODS
#----------------------------------------------------------------------------

#calculate sum of the given array
def calculateSum(arr):
    sum = 0
    #calculate sum of list
    for i in range (len(arr)):
        sum += arr[i]
    return sum



#to compare found better solution with current best solution
def getBetterSolution (A, B, C, bestA, bestB, bestC, diffA, diffB, thirdSum):
    if (diffA <= abs(thirdSum - calculateSum(bestA))) and (diffB <= abs(thirdSum - calculateSum(bestB))):
        bestA = [] 
        bestB = []
        bestC = []

        bestA = A 
        bestB = B
        bestC = C

    return (bestA, bestB, bestC)

#return the difference of the sets with sum/3
def getNewDifference(setArr, thirdSum):
    newDiffArr = [ 0, 0, 0]
    for i in range(3):
        newDiffArr[i] = abs(thirdSum - calculateSum(setArr[i]))

    return newDiffArr



#----------------------------------------------------------------------------
#   MAIN
#----------------------------------------------------------------------------
def main():
    
    #loop for sets of different array
    majorLoop = 100

    #loop for localSearch
    localLoop = 100

    noSolution = 0
    count = 0 #total tests

  

    for i in range(majorLoop):
        f = open("graspResult.txt", "a+")

        
        found = False
        
        
        setArr = []            
        best_diff = 0

        #generate array
        #arr = [27, 36, 41, 100, 50, 15, 42, 14, 49, 13, 45, 8, 4, 9 , 84]
        arr = initializeArr()

        #initialize var to store starting time
        t = time.perf_counter_ns()
        
        #use greedy algo to get partitions
        A, B, C = greedy(arr)

        setArr = [A, B, C]
        bestSetArr = [A, B, C]
       

        #get the difference of each set (difference from the sum/3)
        sum = calculateSum(arr)
        #print("sum: ", sum)
        
        thirdSum = sum/3

        
        #get difference of each partition set based on sum/3
        diffA = abs(thirdSum - calculateSum(A))
        diffB = abs(thirdSum - calculateSum(B))
        diffC = abs(thirdSum - calculateSum(C))
        diffArr = [diffA, diffB, diffC]
       

        #if all difference in all sets are set, return found
        if(diffA == 0 and diffB == 0 and diffC == 0):
            elapsed_time = time.perf_counter_ns() - t
            #f.write(str(elapsed_time/1000000)+"\n")
            found = True
            count += 1
            #print("Solution found: " , bestSetArr)
            #print("diff: ", diffArr)

        else:
            #loop 100 times until best solution is found
            for n in range(localLoop):
                #get sets that will be swapped between their elements
                #getSwapSet returns the INDEX of the setArr, to keep track which sets are used to swapped
                
                #get new difference
                diffArr = []
                diffArr = getNewDifference(setArr, thirdSum)
                if(diffArr[0] == 0 and diffArr[1] == 0 and diffArr[2] == 0):
                    elapsed_time = time.perf_counter_ns() - t
                    #f.write(str(elapsed_time/1000000)+"\n")
                    found = True
                    count += 1
                    break
                        
                swapSet1, swapSet2, remainSet = getSwapSet(diffArr, setArr)
              
                found = False

                #first local search
                setArr[swapSet1], setArr[swapSet2], found = localSearch(setArr[swapSet1], setArr[swapSet2], thirdSum)

     
                #get new difference
                diffArr = []
                diffArr = getNewDifference(setArr, thirdSum)


                #compare current best solution and found best solution,
                #if found best solution is better, replace with current
                betterA, betterB, betterC = getBetterSolution(
                                              setArr[swapSet1], setArr[swapSet2], setArr[remainSet],
                                              bestSetArr[swapSet1], bestSetArr[swapSet2], bestSetArr[remainSet],
                                              diffArr[swapSet1], diffArr[swapSet2],
                                              thirdSum)

                bestSetArr[swapSet1] = copy.deepcopy(betterA)
                bestSetArr[swapSet2] = copy.deepcopy(betterB)
                bestSetArr[remainSet] = copy.deepcopy(betterC)
                #print("after: ", bestSetArr[swapSet1], bestSetArr[swapSet2], bestSetArr[remainSet] )

                if found == True:
                    if(diffArr[remainSet] == 0):
                        elapsed_time = time.perf_counter_ns() - t
                        #f.write(str(elapsed_time/1000000)+"\n")
                        found = True
                        count += 1
                        #print("Solution found: " , bestSetArr)
                        #print("diff: ", diffArr)

                        break
                

            if found == False:
                #print("No solution found, best solution found: ", bestSetArr)
                #print("diff: ", diffArr)
                noSolution += 1
                

                

                
    print("noSol: ", noSolution)
    print("count: ", count)
    f.close()
            
for i in range(500):
    main()
