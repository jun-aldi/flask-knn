from flask import Flask, request
from flask_cors import CORS
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder as Encoder
from sklearn.model_selection import train_test_split
import numpy as np
import joblib
import warnings
warnings.filterwarnings("ignore")

API = Flask("__name__")
CORS(API)

data = pd.read_csv('Data/shet2.csv')
gaya = pd.read_csv('Data/shet2.csv')
data.dropna(inplace=True)
data.drop(['Index'], axis=1, inplace=True)
X = data.drop('Target', axis=1)
y = data['Target']
encoder = Encoder()
y = encoder.fit_transform(y)
scaler = StandardScaler()
X = scaler.fit_transform(X)
KNN = joblib.load('Data/Model.sav')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

def predict(arr):
    array = np.array(arr)
    array = array.reshape(1, -1)
    array = scaler.transform(array)
    y = KNN.predict(array)
    return encoder.inverse_transform(y)[0]

def neigh(arr):
    X_new = np.array([arr])
    distances, indices = KNN.kneighbors(X_new)
    data = []
    for i in range(len(distances[0])):
        data.append(f"Tetangga ke-{i+1}: {gaya['Visual'][indices[0][i]]}, {gaya['Auditorial'][indices[0][i]]}, {gaya['Kinesthetic'][indices[0][i]]}, jarak: {distances[0][i]}, target: {encoder.inverse_transform([y_train[indices[0][i]]])}")
    return data

@API.route("/API/single",methods=['POST'])
def single():
    try :
        json = request.json
        try: arr = [json['V'],json['K'],json['A']]
        except : return "JSON must be {'v':int,'k':int,'a':int}"
        return {"Prediksi":predict(arr), "Data":neigh(arr)}
    except Exception as E:
        print(E)
        return 'Content-Type not supported!, Allowed : JSON'

@API.route("/API/multiple",methods=['POST'])
def multiple():
    try :
        arr = []
        try: 
            for json in request.json['Datas']:
                print(json)
                arr.append([json['V'],json['K'],json['A']])
        except Exception as E :
            print(E)
            return "JSON must be {'Datas':[of multiple {'v':int,'k':int,'a':int}]}"
        return {"Prediksi":[predict(i) for i in arr]}
    except Exception as E: 
        import traceback
        print(traceback.format_exc(E))
        return 'Content-Type not supported!, Allowed : JSON'

app = API.run(debug=True)