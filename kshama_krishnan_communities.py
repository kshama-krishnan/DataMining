import itertools
import random
import sys
import heapq
count=0
clusterDict = {}


def main():
    
    datafile = sys.argv[1]
    noOfClusters = int(sys.argv[2])
    global count
    global clusterDict
    c = 0
    input_file = open(datafile, 'r')
    list_of_datapoints = []
    comb = []
    heap = []
    goldStd = {}
    for line in input_file.readlines():
        itemset = line.strip().split(',')
        lengthOfList = len(itemset)  
        dp1 = Datapoint(count,itemset[:lengthOfList-1], itemset[lengthOfList-1])
        goldStd.setdefault(dp1.classLabel, [])
        goldStd[dp1.classLabel].append(dp1)
        list_of_datapoints.append(dp1)
        clusterDict[count]=[dp1]
        count+=1
        
    

    
if __name__ == '__main__':

    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
       
    