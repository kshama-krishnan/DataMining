import sys
import string
import collections

values={}
inv_map = {}
def setupAlphabetToNumberMapping():
    global values;
    global inv_map
    values = dict()
    index = 0;
    for index, letter in enumerate(string.ascii_lowercase):
        values[letter] = index 
        index = index + 1
    inv_map = {v: k for k, v in values.items()}
    
def xuniqueCombinations(items, n):
    if n==0: yield []
    else:
        for i in xrange(len(items)):
            for cc in xuniqueCombinations(items[i+1:],n-1):
                yield [items[i]]+cc

def hashEquivalent(combo,bucket_size):
    sum = 1;
    for i in range(0,len(combo)):
        sum = sum * getNumberFromAlphabet(combo[i])
    return (sum%bucket_size)
        
def hashEquivalentNumber(combo,bucket_size):
    sum = 1;
    for i in range(0,len(combo)):
        sum = sum * combo[i]
    return (sum%bucket_size)

def getNumberFromAlphabet(it):
    return values[it]

def checkFrequentItemset(d,minimum_support):
    temp = {}
    for key, value in d.iteritems():     
        if value >= minimum_support:
            temp[key]=value
    return temp

def convertToBitmap(d,minimum_support,bucket_size):
    bitmap = [0]*bucket_size
    for key, value in d.iteritems():   
        if(d[key]<minimum_support):
            bitmap[key]=0
        else:
            bitmap[key]=1
    return bitmap

def find_frequent_items_for_k_size(input_file,size,minimum_support,bucket_size):
    input_handler = open(input_file)
    frequency_count = {}
    freq_size1_items = {}
    size2_hash = {}
    bitmap = []
    bitmap = [0]*bucket_size
    
    for line in input_handler.readlines():
        itemset = line.strip().split(',')
        itemset.sort()
            
        if(size == 1):
            for it in itemset:

                num = getNumberFromAlphabet(it)
                if num not in frequency_count:
                    frequency_count[getNumberFromAlphabet(it)]=1;
                else:
                    frequency_count[getNumberFromAlphabet(it)]+=1;
                    
        for combo in xuniqueCombinations( itemset,size+1): 
            combo_value = hashEquivalent(combo,bucket_size); 
            
            if combo_value not in size2_hash:
                size2_hash[combo_value]=1
            else:
                size2_hash[combo_value]+=1
           
          
   
    
                    
    freq_size1_items=checkFrequentItemset(frequency_count,minimum_support)
    bitmap = convertToBitmap(size2_hash,minimum_support,bucket_size);
    
    
    return freq_size1_items,bitmap,size2_hash

def candidateGeneration(input_file,freq_size2_items_check,minimum_support,bucket_size,size):
    input_handler = open(input_file)
    temp = []
    freq_n_itemsets = {}
    notfound = 0;
    mapping = {}
    size3_hash = {}
    for line in input_handler.readlines():
        itemset = line.strip().split(',')
        itemset.sort()
        for it in itemset:
            num = getNumberFromAlphabet(it)
            temp.append(num);
            
        for combo in range(0,len(freq_size2_items_check)):
            for ic in range(0,len(freq_size2_items_check[combo])):
                if(freq_size2_items_check[combo][ic] not in temp):
                    notfound=1
            if notfound ==0:
                combo_value = repr(freq_size2_items_check[combo])
                if combo_value not in freq_n_itemsets:                
                    freq_n_itemsets[combo_value]=1
                    mapping[combo_value]=freq_size2_items_check[combo]
                    
                else:       
                    freq_n_itemsets[combo_value]+=1
                    mapping[combo_value]=freq_size2_items_check[combo]
            notfound = 0
            
        for combo in xuniqueCombinations(temp,size): 
            combo_value = hashEquivalentNumber(combo,bucket_size); 
        
            if combo_value not in size3_hash:
                size3_hash[combo_value]=1
            else:
                size3_hash[combo_value]+=1             
        temp = []
             
    for key, value in freq_n_itemsets.iteritems():   
        if(freq_n_itemsets[key]>=minimum_support):
            temp.append(mapping[key])         
        
    bitmap = convertToBitmap(size3_hash,minimum_support,bucket_size);
     
    return temp,bitmap,size3_hash        
            
def replace_matched_items(word_list, dictionary):
    l = []
    if(any(isinstance(i, list) for i in word_list)):
        for lst in word_list:
            for ind, item in enumerate(lst):
                lst[ind] = dictionary.get(item, item)
        return word_list
    else:
        for ind in range(0,len(word_list)):
            temp=word_list[ind]
            temp1=dictionary[temp]
            l.append(temp1)
        return l;
    




def main():
    input_file = sys.argv[1]
    minimum_support = int(sys.argv[2])
    bucket_size = int(sys.argv[3])
    output_file = open('output_pcy.txt', 'w')
    size = 1;
    freqSet = []
    candidateSet = []
    global values
    global inv_map
    flag = 0;
    size2_hash = {}
    freq_size2_items_check=[];
    size3_hash = {}
    setupAlphabetToNumberMapping();
    freq_size1_items,bitmap,size2_hash = find_frequent_items_for_k_size(input_file,size,minimum_support,bucket_size)
    
    if(len(freq_size1_items)>0):
        freq_list = list(freq_size1_items.keys())    
        list2 = replace_matched_items(freq_list,inv_map)
        candidateSet = freq_list
        
        print >> output_file,list2
        print >> output_file,size2_hash
        
        
        
        while(len(candidateSet)!=0):
            size=size+1
            for combo in xuniqueCombinations(candidateSet,size): 
                combo_value = hashEquivalentNumber(combo,bucket_size); 
                if (bitmap[combo_value] ==1): 
                    for index in range(0,len(combo)):
                        if(combo[index] not in freq_list):
                            flag=1;
                    if(flag==0):
                        freq_size2_items_check.append(combo)
            freqSet,bitmap,size3_hash = candidateGeneration(input_file,freq_size2_items_check,minimum_support,bucket_size,size+1)
            candidateSet = []
            freq_size2_items_check = []
            if(len(freqSet)>0):
                candidateSet=reduce(lambda x,y: x+y,freqSet)
                candidateSet=list(set(candidateSet))
                list1 = sorted(replace_matched_items(freqSet,inv_map))
                print >> output_file,list1
                print >> output_file,size3_hash
            else:
                output_file.close();
                readFile = open("output_pcy.txt")
                lines = readFile.readlines()
                readFile.close()
                w = open("output_pcy.txt",'w')               
                w.writelines([item for item in lines[:-1]])              
                w.close()
                
        
if __name__ == '__main__':
    main()