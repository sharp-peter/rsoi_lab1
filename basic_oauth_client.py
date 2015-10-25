# Basic OAuth Client
# Shows basic information about user

import flask
import requests
import os
import time

from uuid import uuid4

# Client ID and secret
CID = ''
CSC = ''

# Access and refresh tokens
access_token = 'default'
refresh_token = 'default'

# Redirect URI is located on server side
API_URI = 'https://api.imgur.com/'

# Authorization on server side
def authorization():
	app = flask.Flask(__name__)
	
	# Self-explainatory
	def flask_shutdown():
		func = flask.request.environ.get('werkzeug.server.shutdown')
		if func is None:
			raise RuntimeError('Not running with the Werkzeug Server')
		func()
	
		return 'Success: shut down'
	
	# Access and refresh token acquisition
	@app.route('/')
	def token_acquire():
		global access_token
		global refresh_token
		
		auth_data = {
			'client_id': CID,
			'client_secret': CSC,
			'grant_type': 'authorization_code',
			'code': flask.request.args.get('code')
		}
		
		auth_resp = requests.post(API_URI + 'oauth2/token', data=auth_data)
		auth_json = auth_resp.json()
		
		access_token = auth_json['access_token']
		refresh_token = auth_json['refresh_token']
		
		flask_shutdown()
		
		return 'Success: tokens acquired'
	
	app.run(port=5050)

# Starting authentication
def authenticate():
	auth_query = 'client_id=' + CID + '&response_type=code&state' + str(uuid4())
	os.system('start \"\" \"' + API_URI + 'oauth2/authorize?' + auth_query +'\"')
	return authorization()

# Access token reacquisition (for future reference)
def token_reacquire(refresh_token):
	refr_data = {
		'refresh_token': refresh_token, 
		'client_id': CID, 
		'client_secret': CSC,
		'grant_type': 'refresh_token'
	}
	
	refr_resp = requests.post(API_URI + 'oauth2/token', data=refr_data)
	refr_json = refr_resp.json()
	access_token = refr_json['access_token']
	
	return 'Success: access token reacquired'

# Request for user information using access token
def get_user_info():
	reqs_resp = requests.get(API_URI + '3/account/me', headers = {'Authorization': 'Bearer ' + access_token})
	reqs_json = reqs_resp.json()
	reqs_data = reqs_json['data']
	
	if reqs_json['success'] == False:
		print('Error: ', reqs_data['error'])
		return 'Failure'
	
	print('User data:')
	print('User ID:', reqs_data['id'])
	print('User name:', reqs_data['url'])
	print('Created:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(reqs_data['created'])))
	
	return 'Success'
	
# Main function
def main():
	print('ACCESING USER INFORMATION (WITHOUT ACCESS TOKEN)')
	get_user_info()
	
	print('\nACCESING USER INFORMATION (WITH ACCESS TOKEN)')
	authenticate()
	get_user_info()
	
if __name__ == '__main__':
	main()