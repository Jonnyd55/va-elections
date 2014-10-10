import requests
import va_elections as Results

#The URL for Virginia's November General election results, via: http://sbe.virginia.gov/index.php/media-2/election-day-reporting/
data = requests.get('https://voterinfo.sbe.virginia.gov/PublicSite/Public/results/Nov2014General.txt')

'''
I'm going to download the data as a file to my local.
This prevents me hitting the URL everytime I use va_elections and reduces runtime.
'''

file_reader = data.text
with open('data_text.txt', 'w') as f:
	f.write(file_reader)

f.close()

data = 'data_test.txt'

'''
The data file below has random results in it. You can use this as your data file if you want
to test different localities, races, results etc. Using the file from the SBE site above
will return NaN for results before election night, which is what Pandas uses when no value exists.

data = 'test_14.csv'
'''

'''
Instantiate your va_elections module and pass in the data file.
'''

location = Results.Location(data)
race = Results.Race(data)
precinct = Results.Precinct(data)

'''
Define the parameters for each module. This is where your data will be.
'''
precs = precinct.results('location', 'CHESAPEAKE CITY')

va_beach = location.results('PORTSMOUTH CITY')

us_house_10 = race.results(216)

'''
Write the data to files for use.
'''
precinct_data = open('precinct_results.JSON', 'w')
precinct_data.write(precs)
precinct_data.close()


precinct_data = open('location_results.JSON', 'w')
precinct_data.write(va_beach)
precinct_data.close()

precinct_data = open('race_results.JSON', 'w')
precinct_data.write(us_house_10)
precinct_data.close()
