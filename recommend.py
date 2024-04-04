import pickle as pkl
import json
from flask import Flask, request, jsonify
import pandas as pd
import requests
import random;
# from flask import Flask
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
def Sorting(lst):
    lst2 = sorted(lst, key=len)
    return lst2
def Convert(string):
    li = list(string.split(","))
    return li

   
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    data=data['handle']
    # data= Convert(data['questions']) 
    def getdata(handle): 
        url = f'https://codeforces.com/api/user.status?handle={handle}'
        response = requests.get(url)
        data1 = response.json()
        count = 0
        arr2 = []
        for element in data1['result']:
            if element['verdict'] == 'OK':
                if count < 20:
                    count += 1
                    arr2.append(f"{element['problem']['contestId']}{element['problem']['index']}")
                else:
                    break
        rank=0
        l=len(arr2)
        cnt=0
        question_list=[]
        answers=[]
        for i in range(l):
            if(questions_dict[questions_dict['contestId']==arr2[i]].index!="Empty Dataframe"):
                question_index=questions_dict[questions_dict['contestId']==arr2[i]].index[0]
                rank+=questions_dict['rating'][question_index]
                distances=similarity[question_index]
                question_list.append(sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1]))
        rank=int(rank/l)
        for j in range(1,100):
            for i in question_list:       
                if((abs((questions_dict.iloc[i[j][0]].rating)-rank))<=250):
                    answers.append(questions_dict.iloc[i[j][0]].contestId)
        res=[]
        [res.append(x) for x in answers if x not in res]
        res1=[]
        for i in range(30):
            res1.append(res[i])
        res2=[]
        for i in range(10):
            x=random.choice(res1)
            res2.append(x)
        for i in range(len(res2)):
            res2[i]={"questions":res2[i],"name":questions_dict[questions_dict['contestId']==res2[i]].name.values[0],"rating":questions_dict[questions_dict['contestId']==res2[i]].rating.values[0],"tags":questions_dict[questions_dict['contestId']==res2[i]].tags1.values[0]}
        return res2; 
      
    questions_dict=pkl.load(open("questions.pkl","rb"))
    questions_dict=pd.DataFrame(questions_dict)
    similarity=pkl.load(open("similarity.pkl","rb"))  
    prediction = getdata(data)
    return jsonify({"prediction": prediction},)

if __name__ == "__main__":
    app.run()