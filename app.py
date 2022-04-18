from flask import Flask, jsonify, request
from flask_cors import CORS
import testData as d
import sys, json, uuid
from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
from ldap3.core.exceptions import LDAPBindError
from datetime import datetime, timedelta
from pprint import pprint
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

# sanity check route
@app.route('/login', methods=['POST'])
def login():
  response_object = {'status': 'success',
                     'message': 'Auth Accepted'}
  post_data = request.get_json()
  given_login = post_data['user_login']
  login = "KZGROUP\\" + given_login   # domain to database and admin page
  passwd = post_data['pass']
  server = Server('kzgroup.local', get_info=ALL)
  try:
      with Connection(server, user=login,password=passwd,
                      authentication=NTLM,  auto_bind=True) as conn:
          conn.search('DC=kzgroup,DC=local',
              "(&(sAMAccountName=" + given_login + "))",
              attributes=['mail'])
          mailbox = conn.entries[0]['mail']
          # to database
          conn.search('DC=kzgroup,DC=local',
              "(&(sAMAccountName=" + given_login + "))",
              SUBTREE,
              attributes=['memberof'])
          rawGroups=conn.entries[0]['memberof'].values
          groups=[]
          for group in rawGroups:
              groups.append(group.split(',')[0][3:])
          conn.unbind()
          response_object['userlogin'] = given_login  # to database
          response_object['token'] = uuid.uuid4().hex  # to database
          response_object['tokenExp'] = datetime.now() + timedelta(days=2)  # to database
          pprint( response_object['tokenExp'] )
          return jsonify(response_object), 200
  except LDAPBindError as err:
      response_object['message'] = "Invalid Credentials"
      response_object['status'] = "warning"
      return jsonify(response_object), 401

@app.route('/prod_db', methods=['GET','POST'])
def prod_db():
 response_object = {'status': 'success'}
 if request.method == 'POST':
    post_data = request.get_json()
    d.prodData.append({
            'title': post_data.get('title'),
            'responsible': post_data.get('responsible'),
            'production': post_data.get('production')
    })
    response_object['message'] = 'DB added!'
 else:
    response_object['dbs'] = d.prodData
 return jsonify(response_object)

@app.route('/dev_db', methods=['GET','POST'])
def dev_db():
 response_object = {'status': 'success'}
 if request.method == 'POST':
    post_data = request.get_json()
    d.devData.append({
            'title': post_data.get('title'),
            'responsible': post_data.get('responsible'),
            'production': post_data.get('production')
    })
    response_object['message'] = 'DB added!'
 else:
    response_object['dbs'] = d.devData
 return jsonify(response_object)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

