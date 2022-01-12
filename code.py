import requests
import json
from prettytable import PrettyTable
import getopt, sys
import csv
from datetime import datetime

header = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Connection": "keep-alive",
    "Authorization": "token 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"
}

data = []
titles = ["Repository Name", "Open Issues", "Contributors", "IC Ratio"]
# list of command line arguments
argumentList = sys.argv[1:]
# Command line aeguements
options = "co:"
# CSV option used if user wants to write to report else directly print the output
# Org option is used to provide the organization name for which the job needs to be run
long_options = ["CSV", "Org ="]

orgName = ''
writeCSV = False
try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)
    
    for currentArgument, currentValue in arguments:
 
        if currentArgument in ("-c", "--CSV"):
            writeCSV = True
             
        elif currentArgument in ("-o", "--Org"):
            orgName = currentValue
            
except getopt.error as err:
    print (str(err))
    
#check if organization exists
orgExists = requests.get(
    f'https://api.github.com/orgs/{orgName}',
    headers=header)
    
if(orgExists.status_code == 200):
	
	#gets data for all repositories present for the given org
	allRepos = requests.get(
		f'https://api.github.com/orgs/{orgName}/repos',
		headers=header).json()
	
	#calculate ic ratio for each repo and save corresponding data
	for repo in allRepos:
		open_issues = repo["open_issues_count"]
		contributors = len(
		requests.get(
			repo["contributors_url"],
			headers=header).json())
		ic = float("{0:.3f}".format(open_issues / contributors))
		repoData = []
		repoData.append(repo["name"])
		repoData.append(open_issues)
		repoData.append(contributors)
		repoData.append(ic)
		data.append(repoData)
	
	#sort based on the ic ratio
	sorteddata = sorted(data, key=lambda k: k[3], reverse=True)
	final = sorteddata[:5]
	
	if(writeCSV):
		with open("report.csv", "a", newline="") as f:
			writer = csv.writer(f)
			writer.writerow([datetime.now()])
			writer.writerow(titles)
			writer.writerows(final)
		print('Successfully written to CSV file')
	#if csv option not used as arguement directly display the result
	else:
		myTable = PrettyTable(titles)

		for item in final:
			myTable.add_row(item)

		print(myTable)
else:
	print('Given Org does not exists')

