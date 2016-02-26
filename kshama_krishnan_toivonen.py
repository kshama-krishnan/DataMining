import sys
import string
import collections
import random
from collections import Counter
import time
import itertools
freqCount = {}
sampleLines=[]
from copy import deepcopy

def generateFrequentSets(list1,support,size):
    combs =[]
    
    els = [list(x) for x in itertools.combinations(list1, size)]
    combs.extend(els)
    
    return combs


   
def pass1(finalSampleLines,support):

    freqList=[]
   
    freq_list2=[]
    candidateList=[]
    freq2hash={}
    combs = []
    size=1
    extra =[]
    extra1 =[]
    for list1 in finalSampleLines:  
        combs=generateFrequentSets(list1,support,size);
        freqList.extend(combs);
    
    list_of_tuples = [tuple(elem) for elem in freqList]
    dct = dict(Counter(list_of_tuples))
    
    
    for key2,value2 in dct.iteritems():
        if(value2>=support):
            extra.append(sorted(list(key2)))
            candidateList.extend(sorted(list(key2)))
    freq_list2.append(extra)       
    size=2
    while True:
        combs=generateFrequentSets(candidateList,support,size);
        if(len(combs)==0):
            break;
        else:
            candidateList=[]
            temp=[]
            freq2hash={}
            for list1 in finalSampleLines:
                for comboList in combs:
                    if(set(comboList) < set(list1)) or (set(comboList) == set(list1)):
                        if tuple(comboList) not in freq2hash:
                            freq2hash[tuple(comboList)]=1;
                        else:
                            freq2hash[tuple(comboList)]+=1;
            
            
         
            for key2,value2 in freq2hash.iteritems():
                if(value2>=support):
                    
                    extra1.append(sorted(list(key2)))
                    temp.extend(sorted(list(key2)))
                    
            freq_list2.append(sorted(extra1))
            size=size+1
            extra =[]
            extra1 =[]
            candidateList=sorted(list(set(temp)))
  
    
    
    sampleLines=[]
    candidateList=[]
    dct={}
    freqList=[]
    return freq_list2    
    
def getFreqItems(i,freq_list2, allSampleElements):
    frequentSetOld = []
    freqSet = []
    combo1 = []
    for item in freq_list2[i-1]:
        frequentSetOld.append(tuple(item))
    for item in freq_list2[i]: 
        freqSet.append(tuple(item))
        
    for item in itertools.combinations(allSampleElements, i+1):
        combo1.append(item)
    return frequentSetOld,freqSet,combo1    
    

def findNegativeElements(i,currentItems,combo2,frequentSetOld):
    negativeElements=[]
    for item2 in currentItems:
        for item in itertools.combinations(item2, i):
            combo2.append(item)
        flag = 1
        for c2 in combo2:
            if c2 not in frequentSetOld:
                flag = 0
                break
        if flag:
            negativeElements.append(item2)

    return negativeElements


def getNegativeBorder(freq_list2, allSampleElements):
    size = len(freq_list2)
    negativeElements = []
    frequentSetOld = []
    freqSet = []
    combo1 = []
    combo2 = []
    
    for i in range(1, size):  
        frequentSetOld,freqSet,combo1=getFreqItems(i,freq_list2, allSampleElements)
        currentItems = []
        for c1 in combo1:
            if c1 not in freqSet:
                currentItems.append(c1)
            
        negativeElements=findNegativeElements(i,currentItems,combo2,frequentSetOld)

    return negativeElements 

def getLinesUsingRandomSampling(input_file,sampleLines):
    finalSampleLines=[]
    input_handler = open(input_file);
    lines = random.sample(input_handler.readlines(), sampleLines)
    for line in lines:
        itemset = line.strip().split(',')
        itemset.sort()
        finalSampleLines.append(itemset)
    return finalSampleLines
    

            
def main():
    lineCount=0
    input_file = sys.argv[1]
    input_handler = open(input_file);
    minimum_support = int(sys.argv[2]) 
    finalSampleLines=[]
    #support = 1;
    
    
    input_handler = open(input_file)
    for line in input_handler:
        lineCount+=1
    input_handler.close();
    
    probability=0.4
    sampleLines=int(probability*lineCount)
    support = (0.9) * (probability) * minimum_support
    
    it = 0
    
    while(True):
    
        it += 1
        finalSampleLines=getLinesUsingRandomSampling(input_file,sampleLines)
        
        allSampleElements = [y for x in finalSampleLines for y in x]
        allSampleElements = sorted(set(allSampleElements))
        
        input_handler.close();
        freq_list2 =pass1(finalSampleLines,support)
        
        negativeElements = getNegativeBorder(freq_list2, allSampleElements)

        allLines = getLinesUsingRandomSampling(input_file,lineCount)
        allFreqLists = pass1(allLines,minimum_support)
  
        
        flag = 1
        for allFreqList in allFreqLists:
            for candidate in allFreqList:
                if tuple(candidate) in negativeElements:
                    flag = 0
                    break
        if (flag):
            print it
            print probability
            size = len(allFreqLists)
            for i in range(size-1):
                print str(sorted(allFreqLists[i])) + "\n"
            
            break
    
if __name__ == '__main__':
    main()