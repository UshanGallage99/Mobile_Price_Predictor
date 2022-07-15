# import email
# import pyrebase

# config = {
#     'apiKey': "AIzaSyC20S-fGmv7H1diy2GchvIEK9ewMuhsEew",
#     'authDomain': "price-predictor-25e7a.firebaseapp.com",
#     'projectId': "price-predictor-25e7a",
#     'storageBucket': "price-predictor-25e7a.appspot.com",
#     'messagingSenderId': "239075849560",
#     'appId': "1:239075849560:web:3fa8640ca0df8f6226a12d",
#     'databaseURL': ""
# }

# firebase = pyrebase.initialize_app(config)
# auth = firebase.auth()

# email = 'test1@gmail.com'
# password = '12345678'

# user = auth.create_user_with_email_and_password(email,password)
# # print(user)
# info = auth.get_account_info(user['idToken'])
# print(info)