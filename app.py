 
from flask import Flask, render_template, request, redirect,session
import pyrebase
from requests import session
import pickle
import numpy as np

app = Flask(__name__)

def prediction(lst):
    filename = 'model/predictor.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([lst]) 
    return pred_value

def saveData(memory,storage,brand,model,new,used):
    data = {'memory':memory,'storage':storage,'brand':brand,'model':model,'new':new,'used':used}
    print(db.push(data))
    return data

config = {
    'apiKey': "AIzaSyC20S-fGmv7H1diy2GchvIEK9ewMuhsEew",
    'authDomain': "price-predictor-25e7a.firebaseapp.com",
    'projectId': "price-predictor-25e7a",
    'storageBucket': "price-predictor-25e7a.appspot.com",
    'messagingSenderId': "239075849560",
    'appId': "1:239075849560:web:3fa8640ca0df8f6226a12d",
    'databaseURL': "https://price-predictor-25e7a-default-rtdb.firebaseio.com"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db=firebase.database()
app.secret_key = 'secret'

@app.route('/', methods=['POST','GET'])
def index(): 
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password') 
        session = dict() 
        if('user' in session):
                    return render_template("index.html")
        try:
            user = auth.create_user_with_email_and_password(email,password) 
            session['user'] = email
            info = auth.get_account_info(user['idToken'])
            print(info)
            return render_template("index.html")
        except:
            return 'Failed to login'
            
    return render_template("auth.html")

@app.route('/logout')
def logout():
    session = dict() 
    session.pop('user')
    return redirect('/')


@app.route('/home', methods=['POST','GET'])
def home():
    pred_value = 0
    if request.method == 'POST':
        memory = request.form['memory']
        storage = request.form['storage']
        brand = request.form['brand']
        model = request.form['model']
        new = request.form.getlist('new')
        used =request.form.getlist('used')
        print(memory,storage,brand,model,new,used) 

        feature_list = []
        feature_list.append(int(memory))
        feature_list.append(int(storage))
        feature_list.append(len(used))
        feature_list.append(len(new))

        brand_list = ['Apple','Nokia','OPPO','Other','SAMSUNG','Xiaomi','Realme']
        model_list = ['Other', 'Samsung Galaxy','iPhone 11', 'iPhone 12', 'iPhone 6',
       'iPhone 6s', 'iPhone 7', 'iPhone 8',
       'iPhone SE', 'iPhone X', 'iPhone XR',
       'iPhone XS']

        def traverse_list(lst, value):
            for item in lst:
                if item == value:
                    feature_list.append(1)
                else:
                    feature_list.append(0)
        
        traverse_list(brand_list, brand)
        traverse_list(model_list, model)

        pred_value = prediction(feature_list)
        pred_value = np.round(pred_value[0],2) 
        saveData(memory,storage,brand,model,new,used)
    return render_template("index.html",pred_value=pred_value)

if __name__ == '__main__':
    app.run(debug=True)