import itertools
import random
import sys
import heapq
count=0
clusterDict = {}

class Cordinates:
    

    def __init__(self,id1,id2,distance):
        self.id1=id1
        self.id2=id2
        self.distance=distance

    
    def __str__(self):
        return "id1 : ", self.id1.id, "id2 : ", self.id2.id,  ", distance : ", self.distance
        
        
        
    def __lt__(self, other):
        return self.distance < other.distance

    def ___le__(self, other):
        return self.distance <= other.distance
    
    def __eq__(self, other):
        return self.distance == other.distance
    
    def __ne__(self, other):
        return self.distance != other.distance
    
    def __gt__(self, other):
        return self.distance > other.distance
    
    def __ge__(self, other):
        return self.distance >= other.distance



class Datapoint:
    

    def __init__(self,id,dimensions, classLabel=None):
        self.id=id
        self.dimensions = dimensions
        self.classLabel = classLabel
    
    
    def __str__(self):
        return "id : ", self.id, "dimensions : ", self.dimensions,  ", class : ", self.classLabel


    
def findDistance(obj1,obj2):
    
    sum = 0
    if(len(obj1.dimensions)==len(obj2.dimensions)):
        for i in range(0,len(obj1.dimensions)):
            temp  = ((float(obj1.dimensions[i]))-(float(obj2.dimensions[i])))**2
            sum = sum+temp

    return sum**0.5
    
def findCentroid(clusterDataPoints):
    newDimensionList = [0 for x in range(len(clusterDataPoints[0].dimensions))]
    
    for dp in clusterDataPoints:
        for index in range(len(dp.dimensions)):
            newDimensionList[index] += float(dp.dimensions[index])
    
    for index in range(len(newDimensionList)):
        newDimensionList[index] /= float(len(clusterDataPoints))

    return newDimensionList
    
        
    
            

    

def getPairs(l):
    #Standard Pairs
    newList = []
    for key, values in l.iteritems():
        for item in list(itertools.combinations(values, 2)):
            newList.append(item)
    
    return newList

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
        
    for comb in itertools.combinations(list_of_datapoints,2):
        obj1 = comb[0]
        obj2=comb[1]
        distance = findDistance(obj1,obj2)
        
        cordinate=Cordinates(obj1,obj2,distance)
        heapq.heappush(heap, cordinate) 
    obj=None    
    
    
    while(len(clusterDict)!=noOfClusters):    
        
        while True:
            obj = heapq.heappop(heap)
            
            if (obj.id1.id in clusterDict and  obj.id2.id in clusterDict):
                break
        
    
        clusterList = []
        for item in clusterDict[obj.id1.id]:
        
            clusterList.append(item) 
        for item in clusterDict[obj.id2.id]:
        
            clusterList.append(item)  
        centroid = findCentroid(clusterList)
        
        dp=Datapoint(count,centroid)
        
        del clusterDict[obj.id1.id]
        del clusterDict[obj.id2.id]
        clusterDict[count]=clusterList
        count +=1
        for item in list_of_datapoints:
            dist = findDistance(item,dp)
            dp1=Cordinates(item,dp,dist)
            heapq.heappush(heap,dp1)
            
        list_of_datapoints.append(dp)
    
    #Get gold standard pairs
    goldList = getPairs(goldStd)

    #sort the algorithm list
    for key in clusterDict:
        clusterDict[key].sort(key=lambda x: x.id)
        
    
    #Get our list Pairs
    ourList = getPairs(clusterDict)
            
    #common items
    commonLength = float(len(set(goldList).intersection(set(ourList))))
    
    #precision
    print commonLength/len(ourList)
    
    #Recall
    print commonLength/len(goldList)
            
    for key, values in clusterDict.iteritems():
        vals = [x.id for x in values]
        print vals
    
if __name__ == '__main__':

    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
       
    