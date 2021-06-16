import sys
sys.path.append('C:\PythonAnaconda\Lib\site-packages')
from datetime import datetime, timedelta
from cal_setup import get_calendar_service
import list_calendars 
import os

from notion_client import Client
from datetime import datetime, timedelta, date
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

###########################################################################
##### The Set-Up Section. Please follow the comments to understand the code. 
###########################################################################

NOTION_TOKEN = "secret_WJB06DCgeTAXsxz3789oG4wkLDwCeYKn4vUdhhMJKr5" #the secret_something from Notion Integration

database_id = "935349e604ba43cb8ac949bde3323ee6" #get the mess of numbers before the "?" on your dashboard URL

urlRoot = 'https://www.notion.so/yassen/Action-Zone-b24d92e3271d437585af5c6ca5adc38c?' #open up a task and then copy the URL root up to the "p="


##This is where we set up the connection with the Notion API
os.environ['NOTION_TOKEN'] = NOTION_TOKEN
notion = Client(auth=os.environ["NOTION_TOKEN"])
############################################################################
############################################################################

today = date.today()
print("Today's date:", today)

today = today.strftime('%Y-%m-%d')
print()

if True:

    service = get_calendar_service()
    calendars = list_calendars.main()

    while True:
           event_items = []
           w = 0
           for calendar in calendars:
                events = service.events().list(calendarId = calendar['id']).execute()

                for single_item in events['items']:
                    event_items.append(single_item)
                w = w + 1
           
           GCal_today = []
           for event in event_items:
               try:
                   if event['start']['dateTime'][:10] == today :
                       print(event['summary'])
                       GCal_today.append(event)
               except:
                   try:
                       if event['start']['date'][:10] == today :
                           print(event['summary'])
                           GCal_today.append(event)
                   except:
                       try:
                           if event['originalStartTime']['dateTime'][:10] == today :
                               print(event['summary'])
                               GCal_today.append(event)
                       except:
                           if event['originalStartTime']['date'][:10] == today :
                               print(event['summary'])
                               GCal_today.append(event)
           
           page_token = events.get('nextPageToken')
           if not page_token:
               break
    '''
       
    #Create a custom event in GCal (not needed for the final code, just demo)
       #Request Input:
       name = str(input("What is the name of the event?\n"))
       start = str(input("When does it start? (YYYY-MM-DDTHH:MM:SS)\n"))
       end = str(input("When does it end? (YYYY-MM-DDTHH:MM:SS)\n")) 
       colorId = str(input('Choose a colour by number 1-12:\n'))
    
       #calendarId takes the ID of the 🤖 Automated calendar
       event_result = service.events().insert(calendarId='eiatofhjs5umt79mrg37hkc9us@group.calendar.google.com',
           body={
               #"id": "Hello",
               "summary": name,
               "description": 'This is the description',
               "colorId": colorId,
               "start": {"dateTime": start, "timeZone": 'Europe/Sofia'},
               "end": {"dateTime": end, "timeZone": 'Europe/Sofia'},
           }
       ).execute()
 
       print("Created event.")
       print()
       
       
       '''
       
    print()
       #Takes GCal Event and adds it to Notion DB
       
       #Takes all tasks for today from Notion and stores it in Notion_today
    Notion_tasks_today = []
    Notion_today = notion.databases.query(
           **{
            "database_id": database_id,
            "filter": {
                "and": [
                        {
                            "property": 'Do-Date', 
                            "date": {
                                "equals": today
                            }
                        }
                    ]   
                    }
    
            }
       )
       #Prints the different daily tasks
    for Action_index, Action_Item in enumerate(Notion_today['results']):
           Action_Sub = Action_Item['properties']['Action Item']['title'][0]['text']['content']
           print('Task ',str(Action_index + 1),': ', Action_Sub,'\n',sep='')
           Notion_tasks_today.append(Action_Sub)
           
    
    #Add GCal event to Notion
    for GCal_Event in GCal_today:
        #Check if the event name is already on Notion_today
        if GCal_Event['summary'] not in Notion_tasks_today :
            #Add the page
            new_page = notion.pages.create(
                        **{
                            "parent": {
                                "database_id": database_id,
                            },
                            "properties": {
                                'Action Item': {
                                    "type": 'title',
                                    "title": [
                                    {
                                        "type": 'text',
                                        "text": {
                                        "content": GCal_Event['summary'],
                                        },
                                    },
                                    ],
                                },
                                'Do-Date': {
                                    "type": 'date',
                                    'date': {
                                        'start': today,
                                        'end': None, 
                                    }
                                }
                            },
                        },
                    )
           
       
       
#2021-06-09T20:00:00
'''


def main():
   # creates one hour event tomorrow 10 AM IST
   service = get_calendar_service()

   d = datetime.now().date()
   tomorrow = datetime(d.year, d.month, d.day, 10)+timedelta(days=1)
   print(tomorrow)
   start = tomorrow.isoformat()
   print(start)
   end = (tomorrow + timedelta(hours=1)).isoformat()

   #calendarId takes the ID of the 🤖 Automated calendar
   event_result = service.events().insert(calendarId='eiatofhjs5umt79mrg37hkc9us@group.calendar.google.com',
       body={

           "summary": 'Hello',
           "description": 'This is the description',
           #"colorId": 'red',
           "start": {"dateTime": start, "timeZone": 'Europe/Sofia'},
           "end": {"dateTime": end, "timeZone": 'Europe/Sofia'},
       }
   ).execute()
   print(event_result)
   print("created event")
   print()
   print("id: ", event_result['id'])
   print("summary: ", event_result['summary'])
   print("starts at: ", event_result['start']['dateTime'])
   print("ends at: ", event_result['end']['dateTime'])

if __name__ == '__main__':
   main()
'''
