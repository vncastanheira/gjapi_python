# Game Jolt Trophy for Python
# by viniciusepiplon - vncastanheira@gmail.com
# version 1.1
# Python 3.x stable
# Python 2.7 unstable

# This is a general Python module for manipulating user data and
# trophies (achievments) on GameJolt.
# Website: www.gamejolt.com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/lgpl.txt>.

import sys
import hashlib
import json
if sys.hexversion > 0x03000000:
	try:
		import urllib.request
	except:
		raise ImportError
else:
	try:
		import urllib
	except:
		raise ImportError



class GameJoltTrophy(object):
	"""
	The Class constructors. 
	The class requires four essential parameters: user name, user token, game ID
	and private code. Check the API documentation on Game Jolt's website to see
	what those parameters they are. In this code, I used the same names on the 
	site. If you read it, you can understand what's going on here.

	Note that *username* and *user token* can be changed later, but the game id
	and the private key must be defined first, as they won't change.
	"""
	def __init__(self, username, user_token, game_id, private_key):
		super(GameJoltTrophy, self).__init__()
		self.username = username
		self.user_token = user_token
		self.game_id = game_id
		self.private_key = private_key
		self.URL = 'http://gamejolt.com/api/game/v1'

		self.nativeTraceback = False

#====== TOOLS ======#

	# Used for changing users, setting and/or fixing authentications
	def changeUsername(self, username):
		""" 
		Changes the *username* contained on the object 
		Used for changing, setting and/or fixing authentications
		"""
		self.username = username
	# 
	def changeUserToken(self, user_token):
		""" 
		Changes the *user token* contained on the object 
		Used for changing, setting and/or fixing authentications
		"""
		self.user_token = user_token

	def setSignatureAndgetJSONResponse(self, URL):
		"""
		Generates a signature from the url and returns the same address, with the 
		signature added to it.
		All singatures are generated with md5, but can be modified below.
		This is the only function that generates the signature, so changing the
		encoding to SHA1 or other format will affect all URL requests.
		"""
		if sys.hexversion > 0x03000000:
			try:
				link = URL + str(self.private_key)
				link = link.encode('ascii')
				signature = hashlib.md5(link).hexdigest()
				URL += '&'+'signature='+str(signature)
				response = urllib.request.urlopen(URL)
				output = response.read().decode('utf8')
				return json.loads(output)['response']
			except Exception as error: 
				if not self.nativeTraceback:
					return {'success': 'false', 'message': str(error)}
				else:
					raise error
		else:
			try:
				link = URL + str(self.private_key)
				link = link.encode('ascii')
				signature = hashlib.md5(link).hexdigest()
				URL += '&'+'signature='+str(signature)
				response = urllib.urlopen(URL)
				output = response.read().decode('utf8')
				return json.loads(output)['response']
			except Exception as error: 
				if not self.nativeTraceback:
					return {'success': 'false', 'message': str(error)}
				else:
					raise error

	def setNativeTraceback(self, value):
		if not type(value) == bool: self.nativeTraceback = value
		else: raise TypeError

#====== USERS ======#
		
	
	def fetchUserInfo(self):
		"""
		Fetches the infos of a user as a dictionary type.
		**ATTENTION**: it returns a dictionary type value with the key *users*, 
		containing the user being fetched. 
		Right now it only fetches the user stored in the object, but can retrive a 
		list of users. This is not available now, will be implemented later.
		"""
		URL = self.URL+'/users/?format=json&game_id='+str(self.game_id)+'&'+'username='+str(self.username)
		return self.setSignatureAndgetJSONResponse(URL)
			
	
	def authenticateUser(self):
		"""
		Authenticate a user defined in the object variable.
		The purpose of this method is to check if the user's credential 
		(name and token) are valid. Then, you're safe to call the other methods
		Return a boolean type value.
		"""
		URL = self.URL+'/users/auth/?format=json&game_id='+str(self.game_id)+'&'+'username='+str(self.username)+\
		'&'+'user_token='+str(self.user_token)
		return (self.setSignatureAndgetJSONResponse(URL)['success']) == 'true'


#====== TROPHIES ======#

	def fetchTrophy(self, achieved=None, trophy=None):
		"""
		The 'trophy' argument receives a list of one or more ID of trophies to be 
		returned. It ignores the 'achieved' argument, so pass a 'None' value to it.
		where you pass the desired number between the braces, separating each trophy
		ID with commas.
		If 'achieved' is:
		> set to True, only the achieved trophies will be returned
		> set to False, only trophies that the user hasn't achieved yet will be 
		returned
		> set to None (no argument is passed), then all trophies will be retrieved
		"""
		URL = self.URL+'/trophies/?format=json&'+\
		'game_id='+str(self.game_id)+'&'+'username='+str(self.username)+'&'+'user_token='+str(self.user_token)
		if achieved != None:
			URL += '&achieved='
			if achieved == True: URL += 'true'
			if achieved == False: URL += 'false'
		else:
			if trophy != None:
				if type(trophy) == int:
					URL += '&trophy_id='+str(trophy)+'&'
				elif type(trophy) == list:
					miniurl = '&trophy_id='
					for t in trophy:
						miniurl += str(t)+','
					miniurl = miniurl[:1]
					URL += miniurl
				else:
					raise 'Invalid type for trophy: must be int or list.'
		return self.setSignatureAndgetJSONResponse(URL)

	def addAchieved(self, trophy_id):
		"""
		Sets a winning trophy for the user.
		If the parameters are valid, returns True. Otherwise, it returns False.
		"""
		URL = self.URL+'/trophies/add-achieved/?'+\
		'game_id='+str(self.game_id)+'&'+'user_token='+str(self.user_token)+'&'+'username='+str(self.username)+\
		'&'+'trophy_id='+str(trophy_id)
		try:
			return (self.setSignatureAndgetJSONResponse(URL)['success']) == 'true'
		except Exception as error: 
			return {'success': 'false', 'message': str(error)}

#====== SCORES ======#
	
	def fetchScores(self, limit=10, table_id=None, user_info_only=False):
		"""
		The *limit* argument is set to 10 by default, but can't be more than 100. If
		you pass a higher number, the method will automatically set to the maximum
		size.
		*table_id* if for returning scores for a specific table. If no arguments are
		passed (None), it will return all the tables avaliable.
		If *user_info_only* is set to True, only scores for the player stored on the
		object will be returned.
		"""
		URL = self.URL+'/scores/?format=json&game_id='+str(self.game_id)
		if user_info_only:
			URL += '&username='+str(self.username)+'&user_token='+str(self.user_token)
		# ID of the score table
		if table_id:
			URL += '&table_id='+str(table_id)
		# Maximum number of scores should be 100 according with the GJAPI
		if limit > 100:
			limit = 100
		URL += '&limit='+str(limit)
		return self.setSignatureAndgetJSONResponse(URL)

	def addScores(self, score, sort, table_id=None, extra_data='', guest=False, guestname=''):
		"""
		This method adds a score to the player or guest.
		*score* is a string value describing the score value.
		*sort* is the actual score value, a number value. But can be a string too.
		For *table_id*, check the fetchScores method.
		*extra_data* is a string value with any data you would like to store. It
		doesn't appear on the site. 
		If you want to store a score for a guest instead of the user, you:
		> set True to 'guest' parameter.
		> set a string value with the name of the guest on 'guestname'
		"""
		URL = self.URL+'/scores/add/?format=json&game_id='+str(self.game_id)+\
		'&score='+str(score)+'&sort='+str(sort)
		if not guest:
			URL += '&username='+str(self.username)+'&user_token='+str(self.user_token)
		else:
			URL += '&guest='+str(guestname)
		if extra_data:
			URL += '&extra_data='+extra_data
		if table_id:
			URL += '&table_id='+str(table_id)
		return self.setSignatureAndgetJSONResponse(URL)

	def scoreTable(self):
		""" Returns the tables containing the high scores for the game."""
		URL = self.URL+'/scores/tables/?format=json&game_id='+str(self.game_id)
		return self.setSignatureAndgetJSONResponse(URL)

#====== SESSIONS ======#

	def openSession(self):
		"""
		Opens a game session for a particular user. Allows you to tell Game Jolt 
		that a user is playing your game. You must ping the session 
		(**pingSession** method) to keep it active and you must close it when you're 
		done with it. Note that you can only have one open session at a time. 
		If you try to open a new session while one is running, the system will close
		out your current session before opening a new one.
		Return a boolean value: True if a session opened with sucess, False otherwise.
		"""
		URL = self.URL+'/sessions/open/?format=json&game_id='+str(self.game_id)+\
		'&username='+str(self.username)+'&user_token='+str(self.user_token)
		return (self.setSignatureAndgetJSONResponse(URL)['success']) == 'true'

	def closeSession(self):
		"""
		Closes the active section.
		Return a boolean value: True if a session closed with sucess, False otherwise.
		"""
		URL = self.URL+'/sessions/close/?format=json&game_id='+str(self.game_id)+\
		'&username='+str(self.username)+'&user_token='+str(self.user_token)
		return (self.setSignatureAndgetJSONResponse(URL)['success']) == 'true'

	def pingSession(self, active=True):
		"""
		Pings an open session to tell the system that it's still active. If the 
		session hasn't been pinged within 120 seconds, the system will close the 
		session and you will have to open another one. It's recommended that you 
		ping every 30 seconds or so to keep the system from cleaning up your session.
		You can also let the system know whether the player is in an "active" or 
		"idle" state within your game through this call. To do this, you pass an
		argument to the *active* variable. If it is set to True, then the player
		state will be set to **active**. If False, it will be set to **idle**.
		Return a boolean value: True if a session pinged with sucess, False otherwise.
		"""
		URL = self.URL+'/sessions/ping/?format=json&game_id='+str(self.game_id)+\
		'&username='+str(self.username)+'&user_token='+str(self.user_token)
		if active: URL += '&status=active'
		else:	URL += '&status=idle'
		return (self.setSignatureAndgetJSONResponse(URL)['success']) == 'true'

#====== DATA STORAGE ==#
	
	def fetchData(self, key, user_info_only=False):
		"""
		Return the data stored.
		The *key* variable is the identification value for the particular data you
		want to retrieve.
		If you want to return data only for the user stored in the object, the last
		argument is set to True.
		Returns a dictionary containing the data.
		"""
		URL = self.URL+'/data-store/?format=json&game_id='+str(self.game_id)+\
		'&key='+str(key)
		if user_info_only:
			URL += '&username='+str(self.username)+'&user_token='+str(self.user_token)
		return self.setSignatureAndgetJSONResponse(URL)

	def storeData(self, key, data, user_info_only=False):
		"""
		Set a data to be stored.
		The *key* argument is to define the identifier of the data.
		The *data* argument is the data itself, of string type.
		If you wish to pass the data only for this stored in the object, the last
		argument is set to True.
		Return a boolean value: True if the data was stored with sucess, False 
		otherwise.
		"""
		URL = self.URL+'/data-store/set/?format=json&game_id='+str(self.game_id)+\
		'&key='+str(key)+'&data='+str(data)
		if user_info_only:
			URL += '&username='+str(self.username)+'&user_token='+str(self.user_token)
		return (self.setSignatureAndgetJSONResponse(URL)['success']) == 'true'

	def removeData(self, key):
		"""
		Remove a data with the given key.
		*key* is the data identification.
		Return a boolean value: True if the data was removed with sucess, False 
		otherwise.
		"""
		URL = self.URL+'/data-store/remove/?format=json'+'&game_id='+str(self.game_id)+'&key='+str(key)
		return self.setSignatureAndgetJSONResponse(URL) == 'true'

	def getDataKeys(self):
		"""
		Return all the keys avaliable.
		The return type is a dictionary object with a list of dictionaries. Each of
		those dictionaries contains a key with the name **key** and contain it's value.
		Exemple:
		{'keys': [{'key': '1'}, {'key': '2'}, ...], 'success': 'true' }
		"""
		URL = self.URL+'/data-store/get-keys/?format=json'+'&game_id='+str(self.game_id)
		return self.setSignatureAndgetJSONResponse(URL)

