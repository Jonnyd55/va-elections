VA-ELECTIONS
=========

Scraping websites for election results is unreliable and time consuming. Luckily for us in Virginia, the [State Board of Elections][9] releases a [giant text][10] file with election results - updated throughout the night.

Inspired by [python-elections][1] by [Ben Welsh][2], [Ken Shwenke][3] and the wizards on the [L.A. Times data desk][4], I wrote va-elections as a wrapper around the SBE data, aimed at delivering JSON objects. It relies entirely on the [pandas][5] python mondule, so that's a requirement. You need to deliver the static file to the wrapper, and I use [Requests][7] to hit the URL where the data file resides, download it, and pass it to my wrapper.

The files
---
1. __va_elections.py__ - This where the classes reside. I take the CSV file and run analysis on it, depending on which class you choose. You have three classes to choose from, which deliver different results.

 __Location.results()__ - This will return the all of the votes cast, percent of votes each candidate has gathered, along with identifying information and the number of precincts reporting, organized by race.

 __Race.results()__ - Similar to __Location.results()__ but based on a race ID. 

 __Precinct.results()__ - This takes two positional arguments. The 'location' parameter will return race results for every race in that locality, organized by precinct. The 'race' parameter will do the same for a race again organized by precincts.

2. __election_night.py__ An example use of the va-elections wrapper. It returns three JSON files, __location_results.JSON__, __precinct_results.JSON__, __race_results.JSON__ each file returning an example of the classes noted above. 

3. __test_14.csv__ - An example file I populated with test data to demontrate the package.
4. __data_text.txt__ - The file that is created when I run __election_night.py__ - which would be used in a live situation.

Example cases:
---

    import va_elections as Results
    
    #Instaniate your classes
    location = Results.Location(data)
    race = Results.Race(data)
    precincts = Results.Precinct(data)
    
    #Select your location, or a race number
    portsmouth = location.results('PORTSMOUTH CITY')
    us_house_10 = race.results(216)
    suffolk_precs = precincts.results('location', 'SUFFOLK CITY')
    
    portsmouth_results = open('location_results.JSON', 'w')
    portsmouth_results.write(portsmouth)
    portsmouth_results.close()
    
    house_results = open('race_results.JSON', 'w')
    house_results.write(us_house_10)
    house_results.close()
    
    precinct_results = open('precinct_results.JSON', 'w')
    precinct_results.write(suffolk_precs)
    precinct_results.close()
    
    #Check out JSON files for results
    
Caveats
---
1. Take a look at the original [SBE file][8] to get the race numbers you are interested in, indicated by the __officeId__ filed in the data. This is also where you would get the name of your location, as indicated by the __locality_name__ field.
2. I elminiate all of the provisional ballot results when returning the "precincts reporting" field, since in the past the SBE has not used this field to indicate the number of precincts they were reporting.
3. Speed can be a factor depending on the size of the data set. For example, getting race results for a local school board race will take miliseconds, but the senate race may take a few seconds, since it needs to chew on over 2500 precincts.
4. I STRONGLY suggest you test this extensively if you plan to use it in production. It's the first time I've used pandas at any length, and while it passed every test I threw at it, you should make sure it returns the results you are expecting.

If you can get the folks at the Virginia SBE to give you the text files from previous election night results, you can have a lot of fun with this package.

License
----

MIT


[1]:https://github.com/datadesk/python-elections
[2]:https://twitter.com/palewire
[3]:https://twitter.com/schwanksta
[4]:https://github.com/datadesk
[5]:http://pandas.pydata.org/
[7]:http://docs.python-requests.org/en/latest/
[8]:https://voterinfo.sbe.virginia.gov/PublicSite/Public/results/Nov2014General.txt
[9]:http://www.sbe.virginia.gov/
[10]:https://voterinfo.sbe.virginia.gov/PublicSite/Public/results/Nov2014General.txt
