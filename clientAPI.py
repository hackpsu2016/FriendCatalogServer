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
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/api/register')
def Register():
    message = {
        'success': False,
        'message': 'unimplemented'
    }
    return jsonify(results=message)

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

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))