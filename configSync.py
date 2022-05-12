import csv
from notion_client import Client
import os

NOTION_TOKEN = input("What is your secret token (from integration)?") #the secret_something from Notion Integration

database_id = input("What is the URL of your database?") #get the mess of numbers before the "?" on your dashboard URL

os.environ['NOTION_TOKEN'] = NOTION_TOKEN

notion = Client(auth=os.environ["NOTION_TOKEN"])

Notion_today = notion.databases.query(
   **{
    "database_id": database_id,
    "filter": {
        "and": [
            ]   
            }

    }
)

with open('NotionDBdata.csv', mode="w") as file:

	fields = ["Title","Date","Tag","GCal_ID"]

	csvwriter = csv.writer(file)

	csvwriter.writerow(fields)

	rows = [[]]

	properties = Notion_today['results'][0]['properties']
	for prop in properties:
		if properties[prop]['type'] == 'title':
			print("The name of your main property in your Notion Database:",prop)
			titleAns = input("Is this correct? [Y/N]\n")
			if titleAns == "Y" or titleAns == "Yes" or titleAns == "1" or titleAns == 1:
				rows[0].append(prop)
				print(rows)
			else:
				print("Your Database seems to be unsuitable. Use the template to create a working one and try again.")
				break
		if properties[prop]['type'] == "date":
			print(prop)
