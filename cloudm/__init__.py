__version__ = '1.0'

import json
import time
import requests

class CloudM:

	def __init__(self, ip_address, user_login, user_password):
		self.ip_address = ip_address
		self.base_url = 'http://{}/api/v1/automation'.format(ip_address)
		self.login_payload = json.dumps({
			"login": user_login,
			"password": user_password
			})
		self.access_token = None
		self.access_token_expiration = None

		try:
			self.access_token = self.getAccessToken()
			if self.access_token is None:
				raise Exception('Request for token failed.')
		except Exception as e:
			print(e)
		else:
			self.access_token_expiration = time.time() + 3500

	def getAccessToken(self):
		try:
			url = '{}/token'.format(self.base_url)
			headers = {'content-type':'application/json'}
			request = requests.post(url, data=self.login_payload, headers=headers)
			request.raise_for_status()
		except Exception as e:
			print(e)
			return None
		else:
			return 'Bearer '+str(request.json()['accessToken'])

	class Decorators:
		@staticmethod
		def refreshToken(decorated):
			def wrapper(api, *args, **kwargs):
				if time.time() > api.access_token_expiration:
					api.getAccessToken()
				return decorated(api, *args, **kwargs)
			return wrapper


	##########
	# Random #
	##########
	def update_ip_address(self, new_ip_address):
		self.ip_address = new_ip_address
		self.base_url = 'http://{}/api/v1/automation'.format(new_ip_address)


	def update_login(self, new_login, new_password):
		self.login_payload = json.dumps({
			"login": new_login,
			"password": new_password
			})
		self.access_token_expiration = 0


	##################
	# Migrations API #
	##################

	@Decorators.refreshToken
	def list_migrations(self):
		url = '{}/migration'.format(self.base_url)
		headers = {"content-type":"application/json", "Authorization": self.access_token}
		try:
			r = requests.get(url, headers=headers)
			r.raise_for_status()
		except Exception as e:
			print(e)
			return None
		return r.json()['items']

	@Decorators.refreshToken
	def get_migration_details(self, migration_id):
		url = '{}/migration/{}'.format(self.base_url, migration_id)
		headers = {"content-type":"application/json", "Authorization": self.access_token}
		try:
			r = requests.get(url, headers=headers)
			r.raise_for_status()
		except Exception as e:
			print(e)
			return None
		return r.json()

	@Decorators.refreshToken
	def get_migration_history(self, migration_id):
		url = '{}/migration/{}/histories'.format(self.base_url, migration_id)
		headers = {"content-type":"application/json", "Authorization": self.access_token}
		try:
			r = requests.get(url, headers=headers)
			r.raise_for_status()
		except Exception as e:
			print(e)
			return None
		return r.json()['items']

	@Decorators.refreshToken
	def start_migration(self, migration_id):
		url = '{}/migration/{}/start?mode=StartMigration'.format(self.base_url, migration_id)
		headers = {"content-type":"application/json", "Authorization": self.access_token}
		try:
			r = requests.post(url, headers=headers)
			r.raise_for_status()
		except Exception as e:
			print(e)
			return None
		return r.status_code

	@Decorators.refreshToken
	def stop_migration(self, migration_id):
		url = '{}/migration/{}/stop'.format(self.base_url, migration_id)
		headers = {"content-type":"application/json", "Authorization": self.access_token}
		try:
			r = requests.post(url, headers=headers)
			r.raise_for_status()
		except Exception as e:
			print(e)
			return None
		return r.status_code


	##################
	# Statistics API #
	##################

	@Decorators.refreshToken
	def get_total_stats(self, migration_id):
		url = '{}/statistic/{}'.format(self.base_url, migration_id)
		headers = {"content-type":"application/json", "Authorization": self.access_token}
		try:
			r = requests.get(url, headers=headers)
			r.raise_for_status()
		except Exception as e:
			print(e)
			return None
		return r.json()

	@Decorators.refreshToken
	def get_item_stats(self, migration_id, query_state=None):
		if query_state is None:
			url = '{}/statistic/{}/migrationitems'.format(self.base_url, migration_id)
		else:
			url = '{}/statistic/{}/migrationitems?state={}'.format(self.base_url, migration_id, query_state)
		headers = {"content-type":"application/json", "Authorization": self.access_token}
		try:
			r = requests.get(url, headers=headers)
			r.raise_for_status()
		except Exception as e:
			print(e)
			return None
		return r.json()

	@Decorators.refreshToken
	def get_progress_totals(self, migration_id):
		url = '{}/statistic/{}/migrationitems'.format(self.base_url, migration_id)
		headers = {"content-type":"application/json", "Authorization": self.access_token}
		try:
			r = requests.get(url, headers=headers)
			r.raise_for_status()
		except Exception as e:
			print(e)
			return None
		r = r.json()
		progress_totals = {}
		try:
			for i in r['items']:
				if str(i['state']).lower() == 'stopped':
					progress_totals['stopped'] += 1
				if str(i['state']).lower() == 'inprogress':
					progress_totals['inProgress'] +=1
				if str(i['state']).lower() == 'failed':
					progress_totals['failed'] += 1
				if str(i['state']).lower() == 'waiting':
					progress_totals['waiting'] += 1
				if str(i['state']).lower() == 'complete':
					progress_totals['complete'] += 1
		except KeyError:
			return None
		return progress_totals


	################
	# Projects API #
	################

	@Decorators.refreshToken
	def delete_project(self, project_id):
		url = '{}/projects/{}'.format(self.base_url, project_id)
		headers = {"content-type":"application/json", "Authorization": self.access_token}
		try:
			r = requests.delete(url, headers=headers)
			r.raise_for_status()
		except Exception as e:
			print(e)
			return None
		return r.status_code

	@Decorators.refreshToken
	def list_projects(self):
		url = '{}/projects'.format(self.base_url)
		headers = {"content-type":"application/json", "Authorization": self.access_token}
		try:
			r = requests.get(url, headers=headers)
			r.raise_for_status()
		except Exception as e:
			print(e)
			return None
		return r.json()['items']

	@Decorators.refreshToken
	def get_project_details(self, project_id):
		url = '{}/projects/{}'.format(self.base_url, project_id)
		headers = {"content-type":"application/json", "Authorization": self.access_token}
		try:
			r = requests.get(url, headers=headers)
			r.raise_for_status()
		except Exception as e:
			print(e)
			return None
		return r.json()
