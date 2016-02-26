import sys
import string
import collections
from operator import itemgetter
from itertools import islice
uid_dict={}

def find_average_rating(user1):   
    global uid_dict
    
    ratingCount=0.0
    count=0.0
    for key in uid_dict:
        if key==user1:
            values=uid_dict.get(user1)
            for value in values: 
                for movie,rating in value.iteritems():
                    count=count+1.0;
                    ratingCount+=float(rating)
            break
                
    avg_rating = ratingCount/count
    return avg_rating
  

def pearson_correlation(user1, user2):   
    global uid_dict
    avg_rating1 = find_average_rating(user1)
    avg_rating2 = find_average_rating(user2)
    user1values=[]
    user2values=[]
    user1valuesDict={}
    user2valuesDict={}
    num=0.0
    denom=0.0
    user1Calc=0.0
    user2Calc=0.0
    fraction=0.0
    user1values=uid_dict.get(user1)

    user2values=uid_dict.get(user2)
        
    for d in user1values:
        user1valuesDict.update(d)

    for d in user2values:
        user2valuesDict.update(d)   
    
    

    
    for name in set(user1valuesDict).intersection(set(user2valuesDict)):
       
        
        num+=(float(user1valuesDict[name])-avg_rating1)*(float(user2valuesDict[name])-avg_rating2)
        
    for name in set(user1valuesDict).intersection(set(user2valuesDict)):
        user1CalcTemp = (float(user1valuesDict[name])-avg_rating1)**2
        user1Calc+=user1CalcTemp
        
        user2CalcTemp = (float(user2valuesDict[name])-avg_rating2)**2
        user2Calc+=user2CalcTemp
        
    denom=(user1Calc**0.5)*(user2Calc**0.5)
        
    fraction=num/denom
    return fraction

    
    
    
    
    
def K_nearest_neighbors(user1, k): 
    global uid_dict
    final_list = []
    neighbour_list = []
    for key in uid_dict:
        neighbour_dict = {}
        if(key != user1):
            neighbour_dict['user']=key            
            neighbour_dict['pearson_correlation']=pearson_correlation(user1, key)
            neighbour_list.append(neighbour_dict)
           
            
    final_neighbours = sorted(neighbour_list,key=itemgetter('pearson_correlation'),reverse=True)
   
    iterator = islice(final_neighbours, 10)
    for item in iterator:
        final_list.append(item)
    
    
    return final_list


def Predict(user_id, movie_name, neighbour_list):
    
    global uid_dict
    num=0.0
    den=0.0
    common_users=[]

    for d in neighbour_list:
        user_id=d['user']
        
        
        movie_names=uid_dict[user_id]
        
        for item in movie_names:
            flag=False
            for key in item:
                
                if(key==movie_name):
                    common_users.append(d)
                    flag=True
                    break
                
                if(flag):
                    break;
                
    for item in common_users:
        den+=item['pearson_correlation']
        temp = uid_dict[item['user']]
        
        for i in temp:
            flag=False
            for key,value in i.iteritems():
                
                if(key==movie_name):
                    num+=float(value)*item['pearson_correlation']
                    flag=True
                    break
                
                if(flag):
                    break;
        
    if(den==0):
        return 0
    else:
        return num/den
        
            
        




def main():
    input_file = sys.argv[1]
    user_id = sys.argv[2]
    movie_name = sys.argv[3]
    k = sys.argv[4]
    neighbour_list = []
    input_handler = open(input_file, 'r')
  
    
    global uid_dict
    for line in input_handler.readlines():
        movie_id={}
        line =  [splits for splits in line.strip().split("\t") if splits is not ""]
        movie_id[line[2]]=line[1];
        uid_dict.setdefault(line[0],[])
        uid_dict[line[0]].append(movie_id)
          
     
    neighbour_list = K_nearest_neighbors(user_id, k)
    for item in neighbour_list:
        print item['user'], item['pearson_correlation']
    print "\n"
    
    fraction=Predict(user_id, movie_name, neighbour_list)
    print fraction
    
      
if __name__ == '__main__':
    main()