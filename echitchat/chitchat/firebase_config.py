import pyrebase

firebase_config = {
    "apiKey": "your-apiKey",
    "authDomain": "your-authDomain",
    "databaseURL": "your-databaseURL",
    "projectId": "your-projectId",
    "storageBucket": "your-storageBucket",
    "messagingSenderId": "your-messagingSenderId",
    "appId": "your-appId",
    "measurementId": "your-measurementId"
}

firebase = pyrebase.initialize_app(firebase_config)
