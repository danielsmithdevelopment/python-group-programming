# Required imports
import os
import json
import pyrebase
from flask import Flask, request, jsonify
from firebase_admin import credentials, auth, firestore, initialize_app
from functools import wraps

# Initialize Flask app
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('config/see-the-greens-firebase-adminsdk-5fe3q-84ba5e43d0.json')
firebase = initialize_app(cred)
db = firestore.client()
trade_ref = db.collection('trades')
pb = pyrebase.initialize_app(json.load(open('config/firebase-config.json')))

# Middleware to check tokens and protect routes
def check_token(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if not request.headers.get('authorization'):
            return {'message': 'No token provided'},400
        try:
            user = auth.verify_id_token(request.headers['authorization'])
            request.user = user
        except:
            return {'message':'Invalid token provided.'},400
        return f(*args, **kwargs)
    return wrap

@app.route('/add', methods=['POST'])
@check_token
def create():
    """
        create() : Add document to Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        id = request.json['id']
        trade_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/list', methods=['GET'])
@check_token
def read():
    """
        read() : Fetches documents from Firestore collection as JSON.
        trade : Return document that matches query ID.
        all_trades : Return all documents.
    """
    try:
        # Check if ID was passed to URL query
        trade_id = request.args.get('id')
        if trade_id:
            trade = trade_ref.document(trade_id).get()
            return jsonify(trade.to_dict()), 200
        else:
            all_trades = [doc.to_dict() for doc in trade_ref.stream()]
            return jsonify(all_trades), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/update', methods=['POST', 'PUT'])
@check_token
def update():
    """
        update() : Update document in Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        trade_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/delete', methods=['GET', 'DELETE'])
@check_token
def delete():
    """
        delete() : Delete a document from Firestore collection.
    """
    try:
        # Check for ID in URL query
        trade_id = request.args.get('id')
        trade_ref.document(trade_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

# #Api route to sign up a new user
# @app.route('/signup')
# def signup():
#     email = request.form.get('email')
#     password = request.form.get('password')
#     if email is None or password is None:
#         return {'message': 'Error missing email or password'},400
#     try:
#         user = auth.create_user(
#                email=email,
#                password=password
#         )
#         return {'message': f'Successfully created user {user.uid}'},200
#     except:
#         return {'message': 'Error creating user'},400

#Api route to get a new token for a valid user
@app.route('/token', methods=['POST', 'PUT'])
def token():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = pb.auth().sign_in_with_email_and_password(email, password)
        jwt = user['idToken']
        return {'token': jwt}, 200
    except:
        return {'message': 'There was an error logging in'},400

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)