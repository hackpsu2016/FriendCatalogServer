# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import requests
from flask import Flask, jsonify, request
from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired
import couchdb
import config
from config import db_name
import twitter_helper

app = Flask(__name__)


# cl_username = '91819ede-4166-4871-bdb4-c58ee8e44e2c-bluemix'
# cl_password = "77f3fee25e14cd0c13c8ec0cf6d9b8aa364ef63c53dd5d3c257570916855a553"


def get_db(table):
    couch = couchdb.Server(config.db_url)
    couch.resource.credentials = (config.db_username, config.db_password)
    print(config.db_username, config.db_password)
    db = couch[table]
    return db

@app.route('/dbquery/<query>')
def query_db(query):
    # Select db that has this query
    db = get_db(db_name)
    map_fun = '''function(doc) {
        if (doc.email == query)
            emit(doc.name, null);
    }
    '''
    for id in db:
        doc = db[id]
        info = {key: doc[key] for key in doc}
        print(id, info)
    return str(db.name)

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/api/register')
def Register():
    message = {
        'success': False,
    }
    db = get_db(db_name)
    username = request.args.get('username')
    password = request.args.get('password')
    email = request.args.get('email')
    print(db.get(username))
    if db.get(username):
        message["message"]="username already exists"
        return jsonify(results=message)
    doc_id, doc_rev = db.save({'_id':username,'email':email,'password':password})
    message["success"] = True
    
    return jsonify(results=message)

@app.route('/api/login')
def Login():
    message = {
        'success': False,
        'message': 'Username and password combination do not match'
    }
    query_username = request.args.get('username')
    query_password = request.args.get('password')
    db = get_db(db_name)
    if db.get(query_username) and db[query_username]["password"] == query_password:
        message['success'] = True
        message['message'] = ""
        message['token'] = get_auth_token()
        db.save({'token': message['token']})
        return jsonify(message)
    return jsonify(message)

@app.route('/api/twitter/<username>')
def getTwitter(username):
    """
    Test function to see if scraping is working.
    Get twitter JSON from api
    :param username:
    :return:
    """
    message = {
        'success': False,
        'message': 'Not an active username or twitter account'
    }
    db = get_db(db_name)
    if db.get(username):
        handle = db[username]['twitter']
    data = twitter_helper.process_tweets(handle)
    message['success'] = True
    return data

@app.route('/api/personality/<username>')
def inject_personality(username):
    """
    Injects Big Five personality traits into the database by scraping their twitter data and using IBM's
    Personality Insights to calculate the traits.
    :param username:
    :return:
    """
    from personality_insights import send_pi_request, extract_personality
    message = {
        'success': False,
        'message': 'Error: Personality not injected into {}. User may not exist or extraction failed'.format(username)
    }
    db = get_db(db_name)
    doc = db.get(username)
    if doc:
        # Extract personality dictionary
        handle = db[username]['twitter']
        pi_data = send_pi_request(handle)
        personality = extract_personality(pi_data)
        # Why isn't this working? Need to insert
        doc['personality'] = personality
        db.save(doc)
        message['success'] = True
        message['message'] = 'Personality: {}'.format(personality)
        return jsonify(message)
    return jsonify(message)


@app.route('/api/token')
def get_auth_token():
    token = generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })

@app.route('/api/myprofile')
def MyProfile():
    profiledata = {
        'success': False,
        'message': 'unimplemented'
    }
    return jsonify(results=profiledata)


@app.route('/api/editprofile')
def EditProfile():
    editmessage = {
        'success': False,
        'message': 'unimplemented'
    }
    return jsonify(results=editmessage)

@app.route('/api/register')
def Search():
    searchresults = {
        'success': False,
        'message': 'unimplemented',
        'list': [
            {'name': 'John', 'age': 28},
            {'name': 'Bill', 'val': 26}
        ]
    }
    return jsonify(results=searchresults)

@app.route('/api/viewprofile/<id>')
def ViewProfile():
    profiledata = {
        'success': False,
        'message': 'unimplemented'
    }
    return jsonify(results=profiledata)

@app.route('/api/getfriends')
def GetFriends():
    friendlist = {
        'success': False,
        'message': 'unimplemented'
    }
    return jsonify(results=friendlist)

@app.route('/api/resquestfriend/<id>')
def RequestFriend():
    friendrequest = {
        'success': False,
        'message': 'unimplemented'
    }
    return jsonify(results=friendrequest)

##############################
#       static methods
##############################

def generate_auth_token(self, expiration = 600):
        s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

##############################
#            main
##############################

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
