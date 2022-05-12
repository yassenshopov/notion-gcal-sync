############################################################################
##### Import section.
##### Necesary PIPs: time, datetime, notion_client, 
##### google-api-python-client, os.
############################################################################

from datetime import date
import time
from cal_setup import get_calendar_service
import list_calendars 
import os
from notion_client import Client

###########################################################################
##### Setting Up. Here you need to provide your Notion credentials. 
###########################################################################

NOTION_TOKEN =  #the secret_something from Notion Integration

database_id =  #get the mess of numbers before the "?" on your dashboard URL

##### This is where we set up the connection with the Notion API

os.environ['NOTION_TOKEN'] = NOTION_TOKEN

notion = Client(auth=os.environ["NOTION_TOKEN"])

##### This is where you enter the names of your Notion Columns:

title = ## Put the 'Title' Property name here

timing = ## Put the 'Date' Property name here

tag = ## Put the 'Tag' (multi-select) Property name here

############################################################################
##### Acquiring today's date to sync only today's tasks.
##### Timezone is determined here.
############################################################################

today = date.today()
print("Today's date:", today)
today = today.strftime('%Y-%m-%d')
tz = time.tzname[time.daylight]
print(tz)
if tz == "BST":
    tz = "Europe/London"
elif tz == "EEST":
    tz = "Europe/Sofia"

print(tz,"\n")

############################################################################
##### Run cal_setup to provide GCal access.
############################################################################

service = get_calendar_service()
calendarList = list_calendars.list_calendars()

############################################################################
##### Use the list "exceptions" to specify calendars you do not want to sync.
##### Enter their titles in quotation marks, separated by commas.
############################################################################
	
exceptions = []

############################################################################
##### Initialise empty lists for future use.
############################################################################

eventsGCal = []
eventsGcalToday = []
	
for calendar in calendarList:
	if calendar['summary'] in exceptions:
		calendarList.remove(calendar)

	############################################################################
	##### Take all the events from GCal's Calendars and filter them for today.
	############################################################################

	else:
		events = service.events().list(calendarId = calendar['id']).execute()
		for event in events['items']:
			event['calendarId'] = calendar['id']
			eventsGCal.append(event)

for event in eventsGCal:

############################################################################
##### Check for cancelled recurring events.
############################################################################

	if event['status'] != 'cancelled':

		############################################################################
		##### Case 1: Full-day events. ('start'['date']).
		############################################################################

		try:
			if event['start']['date'][:10] == today:
				eventsGcalToday.append(event)
				print('Case 1:',event)
				print(event['start']['date'],end="\n\n")
		except:

			############################################################################
			##### Case 2: Scheduled during-the-day events. ('start'['dateTime']).
			############################################################################

			try:
				if event['start']['dateTime'][:10] == today:
					eventsGcalToday.append(event)
					print('Case 2:',event)
					print(event['start']['dateTime'],end="\n\n")
			except:
				print('"start" Exception Occured')

############################################################################
##### Copy the events data from eventsGCalToday to Notion DB.
##### Sanity Check #1: If eventsGCalToday is empty.
##### Sanity Check #2: If event description has Sync Check (Synced: ✅).
############################################################################

if eventsGcalToday != []:
	for GCalEvent in eventsGcalToday:

		try:
			if '[Synced ✅]' not in GCalEvent['description']:

				############################################################################
				##### Case 1: Full-day events. ('start'['date']).
				############################################################################

				try:
					new_page = notion.pages.create(

						**{
						"parent": {"database_id": database_id},
						"properties":{
							'GCal_ID': {'rich_text': [{'text': {'content': GCalEvent['id']}}]},
			                title: {"title": [{"text": {"content": GCalEvent['summary']}}]},
			                tag: {'multi_select':[{'name': GCalEvent['organizer']['displayName']}]},
							timing: {'date': {'start': GCalEvent['start']['date'][:10],'end': None}}

						}
						}

					)

					############################################################################
					##### Update GCal event with [Synced ✅] mark in description.
					############################################################################

					updateGCal = service.events().patch(calendarId = GCalEvent['calendarId'], eventId = GCalEvent['id'], body={"description": '[Synced ✅]',}).execute()

				############################################################################
				##### Case 2: Scheduled during-the-day events. ('start'['dateTime']).
				############################################################################

				except:
					new_page = notion.pages.create(

						**{
						"parent": {"database_id": database_id},
						"properties":{
							'GCal_ID': {'rich_text': [{'text': {'content': GCalEvent['id']}}]},
			                title: {"title": [{"text": {"content": GCalEvent['summary']}}]},
			                tag: {'multi_select':[{'name': GCalEvent['organizer']['displayName']}]},
							timing: {'date': {'start': GCalEvent['start']['dateTime'],'end': GCalEvent['end']['dateTime']}}

						}
						}

					)

					############################################################################
					##### Update GCal event with [Synced ✅] mark in description.
					############################################################################

					updateGCal = service.events().patch(calendarId = GCalEvent['calendarId'], eventId = GCalEvent['id'], body={"description": '[Synced ✅]',}).execute()

			'''

			else:

			############################################################################
			##### This part of the code updates the data of already-synced events.
			############################################################################

				############################################################################
				##### Case 1: Full-day events. ('start'['date']).
				############################################################################

				try:
					new_page = notion.pages.update(

						**{
						"parent": {"database_id": database_id},
						"properties":{
							'GCal_ID': {'rich_text': [{'text': {'content': GCalEvent['id']}}]},
			                title: {"title": [{"text": {"content": GCalEvent['summary']}}]},
			                tag: {'multi_select':[{'name': GCalEvent['organizer']['displayName']}]},
							timing: {'date': {'start': GCalEvent['start']['date'][:10],'end': None}}

						}
						}

					)

		'''

		except:

			############################################################################
			##### Case 1: Full-day events. ('start'['date']).
			############################################################################

			try:
				new_page = notion.pages.create(

					**{
					"parent": {"database_id": database_id},
					"properties":{
						'GCal_ID': {'rich_text': [{'text': {'content': GCalEvent['id']}}]},
		                title: {"title": [{"text": {"content": GCalEvent['summary']}}]},
		                tag: {'multi_select':[{'name': GCalEvent['organizer']['displayName']}]},
						timing: {'date': {'start': GCalEvent['start']['date'][:10],'end': None}}

					}
					}

				)

				############################################################################
				##### Update GCal event with [Synced ✅] mark in description.
				############################################################################

				updateGCal = service.events().patch(calendarId = GCalEvent['calendarId'], eventId = GCalEvent['id'], body={"description": '[Synced ✅]',}).execute()

			############################################################################
			##### Case 2: Scheduled during-the-day events. ('start'['dateTime']).
			############################################################################

			except:
				new_page = notion.pages.create(

					**{
					"parent": {"database_id": database_id},
					"properties":{
						'GCal_ID': {'rich_text': [{'text': {'content': GCalEvent['id']}}]},
		                title: {"title": [{"text": {"content": GCalEvent['summary']}}]},
		                tag: {'multi_select':[{'name': GCalEvent['organizer']['displayName']}]},
						timing: {'date': {'start': GCalEvent['start']['dateTime'],'end': GCalEvent['end']['dateTime']}}
					}
					}
				)

				############################################################################
				##### Update GCal event with [Synced ✅] mark in description.
				############################################################################

				updateGCal = service.events().patch(calendarId = GCalEvent['calendarId'], eventId = GCalEvent['id'], body={"description": '[Synced ✅]',}).execute()


