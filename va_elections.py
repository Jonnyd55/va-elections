import pandas as pd
import json


class Location:
	def __init__(self, data):
		self.data = pd.read_csv(data)

	def results(self, location):
		df = self.data[self.data.locality_name == location]

		#This gets me the votes and vote precentages for each candidate in every race in the locality.
		results = df.groupby(['officeId','candidateId','candidate_name', 'party', 'office_name'], as_index=False)['total_votes'].sum()

		#Getting the percentage of votes for each candidate in each race in each locality
		results['vote_pct'] = results['total_votes'] / results.groupby('officeId')['total_votes'].transform('sum')

		#Getting precincts results for every race in location
		def get_precincts(prec):
			reported = {'reported':prec.total_votes.count(),
						'total': prec.total_votes.notnull().count()}
			return reported
		#Filter out the ###PROV district
		precincts = df[df.precinct_code != '###PROV']

		precincts = precincts.groupby(['officeId','precinct_name'], as_index=False).total_votes.sum()

		# Apply the get_results function to build the district reporting data
		precincts_reporting = precincts.groupby(['officeId']).apply(get_precincts)

		#Now we will load up the data object with the results. 
		#It will also include the precincts reporting.

		data_dump = {}

		#formatting the data, loading up the dictionary
		for key, group in results.groupby('officeId'):
			data_dump[str(key)] = group.to_dict('records')

		data_dump['precincts'] = json.dumps(precincts_reporting.to_json(), indent=4)

		s = json.dumps(data_dump, indent=4)
		s = s.replace("\\","").replace('""', '')
		
		return s


class Race():

	def __init__(self, data):
		self.data = pd.read_csv(data)

	def results(self, race):

		single_race = self.data[self.data.officeId == race]

		results = single_race.groupby(['officeId','candidateId','candidate_name', 'party', 'office_name'], as_index=False)['total_votes'].sum()

		#Getting the percentage of votes for each candidate
		results['vote_pct'] = results['total_votes'] / results.groupby('officeId')['total_votes'].transform('sum')

		def get_precincts(prec):
			reported = {'reported':prec.total_votes.count(),
						'total': prec.total_votes.notnull().count()}
			return reported
		
		#Filter out the ###PROV district
		precincts = single_race[single_race.precinct_code != '###PROV']

		#Need to create unique values for the precinct names to get precinct counts later
		precincts['prec_check'] = precincts['precinct_name'] + precincts['locality_name']

		#Grouping precincts and applying get_results to build the data objects
		precincts = precincts.groupby(['officeId','precinct_name', 'prec_check'], as_index=False)['total_votes'].sum()
		precincts_reporting = precincts.groupby(['officeId']).apply(get_precincts)

		#Data object container
		data_dump = {}
		#formatting the data, loading up the dictionary
		for key, group in results.groupby('officeId'):
			data_dump[str(key)] = group.to_dict('records')

		data_dump['precincts'] = json.dumps(precincts_reporting.to_json(), indent=4)
		
		s = json.dumps(data_dump, indent=4)
		s = s.replace("\\","").replace('""', '')

		return s

class Precinct():
	def __init__(self, data):
		self.data = pd.read_csv(data)

	def results(self, race_type, selection):

		try:
			if race_type == "race":
				result_data = self.data[self.data.officeId == int(selection)]
			elif race_type == "location":
				result_data = self.data[self.data.locality_name == selection]
		except ValueError:
			print 'You must choose a type of result dictionary. You can use "race" or "location"'

		
		result_data = result_data[result_data.precinct_code != '###PROV']
		precincts = result_data.groupby(['precinct_name', 'candidateId', 'officeId'], as_index=False)['total_votes'].sum()

		precs = {}
		for key, group in precincts.groupby('precinct_name'):
			precs[str(key)] = group.to_dict('records')


		prec_data = []
		for key, val in precs.iteritems():
			pre_data_list = []
			precinct_bucket = {}
			
			for data in val:
				place = data['precinct_name']
				precinct_bucket[data['officeId']] = []

			for key, prec in precinct_bucket.iteritems():
				for results in val:
					if key == results['officeId']:
						prec.append(results)
			
			for key, val in precinct_bucket.iteritems():
				race_obj = {key: val}
				pre_data_list.append(race_obj)
			
			if place == '##Central Absentee':
				place = 'Absentee'
			else:
				place = place.split('-')
				place = place[1].strip()

			precinct = {place: pre_data_list}
			prec_data.append(precinct)
			
		s = json.dumps(prec_data, indent=4)
		s = s.replace("\\","").replace('""', '')

		return s




