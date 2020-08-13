import datetime
import pandas as pd
import numpy as np
import sklearn as sks
import nltk
from datetime import timedelta
from datetime import datetime , date
import string
from collections import Counter

from fastapi import FastAPI
from typing import Optional

from pydantic import BaseModel

app = FastAPI()

data_train=pd.read_csv('drugsComTrain_raw.tsv', sep='\t')

class Item(BaseModel):
    name: list = []
    



def test(data_train, item):
    print(type(item))

    data_train['date']=pd.to_datetime(data_train['date'] , infer_datetime_format=True)


    score = data_train.rating * data_train.usefulCount
    data_train['Score'] = score
    sample_data2 = data_train[['drugName' , 'condition','review', 'rating', 'usefulCount','Score' ]]
    result = pd.DataFrame(columns = ['drugName' , 'condition','review' 'rating', 'usefulCount','Score' ])
    resultt1 = []
    resultt2 = []
 


    user_input = item
    for xx in user_input:
        print(len(user_input))
        print(xx)
        
        for i in sample_data2 :
            result = sample_data2['condition'].isin([xx])


        dn=pd.DataFrame(sample_data2[result])



        med_count=Counter(dn['drugName'])
        #print(med_count)
        dd = pd.Series(med_count)
        dd.sort_values(ascending=False, inplace=True)
        #print("dd" , dd)

        # doc=pd.DataFrame.from_dict(med_count,orient='index').reset_index()  
        # doc.set_axis(['drugName','Frequency' ] , axis =1 , inplace =True)


        # doc.sort_values(by=['Frequency'] , ascending=False , inplace=True)
        #print(doc)
        # doc_frame = pd.DataFrame(doc)

    
        #patient
        dn.sort_values(by=['Score'] , ascending=False , inplace=True)
        pat = dn.drop_duplicates(subset ="drugName")
        pat_final=pat.drop(labels = ['condition' , 'usefulCount' ,'rating' , 'review'  ] ,axis=1)
        #print(pat_final)

       
        
    
        docc  = dd.to_frame(name="vals")
        #print(docc)
        docc = docc.vals.iloc[:2]
        docc.to_dict()
        #print(docc)
        #print(type(docc))
        docc = docc.astype('object')


        #print("hhbhhh",type(docc))


        
        patt = pat_final.drugName.iloc[:2]
        
        
        
        

        
        
        

        resultt1.append(docc)
        resultt2.append(patt)
        
    #print("AMAL2" , resultt2)
    #print("AMAL1" , resultt1)
    return(resultt1, resultt2)





@app.post("/predict/")
async def create_item(item: Item):
    return(test(data_train, item.name))
 

    