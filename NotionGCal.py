import sys
sys.path.append('C:\PythonAnaconda\Lib\site-packages')
from datetime import date
from cal_setup import get_calendar_service
import list_calendars 
import os

from notion_client import Client

import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

#######################################

CREDENTIALS_FILE = 'credentials.json'

NOTION_TOKEN =  #The secret code from Notion Integration (it should look like this: NOTION_TOKEN = "secret_XXXXXXXXXXXXX")

database_id =  #Get the string of numbers before the "?" on your Notion dashboard URL (it should look like this: database_id = "xxxxxxxxxxxxxxxxxxxxxxxxxx")

urlRoot =  #open up a task and then copy the URL root up to the "p=" (it should look like this: urlRoot = "https://www.notion.so/xxxxx/xxxxxx-xxxxxxxxx?")

dateProperty =  #The name of the 'Date' property for your items in your Notion Database (it should look like this: dateProperty = 'Date')

nameProperty =  #The name of the 'Title' property for your items in your Notion Database (it should look like this: nameProperty = 'Name')

########################################

def get_calendar_service():
   creds = None
   # The file token.pickle stores the user's access and refresh tokens, and is
   # created automatically when the authorization flow completes for the first
   # time.
   if os.path.exists('token.pickle'):
       with open('token.pickle', 'rb') as token:
           creds = pickle.load(token)
   # If there are no (valid) credentials available, let the user log in.
   if not creds or not creds.valid:
       if creds and creds.expired and creds.refresh_token:
           creds.refresh(Request())
       else:
           flow = InstalledAppFlow.from_client_secrets_file(
               CREDENTIALS_FILE, SCOPES)
           creds = flow.run_local_server(port=0)

       # Save the credentials for the next run
       with open('token.pickle', 'wb') as token:
           pickle.dump(creds, token)

   service = build('calendar', 'v3', credentials=creds)
   return service

def list_calendars():
   service = get_calendar_service()
   # Call the Calendar API
   #print('Getting list of calendars')
   calendars_result = service.calendarList().list().execute()

   calendars = calendars_result.get('items', [])

   if not calendars:
    #   print('No calendars found.')
        print()
   for calendar in calendars:
       summary = calendar['summary']
       id = calendar['id']
       #primary = "Primary" if calendar.get('primary') else ""
       #print("%s\t%s\t%s" % (summary, id, primary))
   return calendars

os.environ['NOTION_TOKEN'] = NOTION_TOKEN
notion = Client(auth=os.environ["NOTION_TOKEN"])

today = date.today()
print("Today's date:", today)

today = today.strftime('%Y-%m-%d')
print()

if True:

    service = get_calendar_service()
    calendars = list_calendars()

    while True:
           event_items = []
           for calendar in calendars:
                events = service.events().list(calendarId = calendar['id']).execute()

                for single_item in events['items']:
                    event_items.append(single_item)
           
           GCal_today = []
           for event in event_items:
               try:
                   if event['start']['dateTime'][:10] == today :
                       print(event['summary'])
                       print()
                       GCal_today.append(event)
               except:
                   try:
                       if event['start']['date'][:10] == today :
                           print(event['summary'])
                           print()
                           GCal_today.append(event)
                   except:
                       try:
                           if event['originalStartTime']['dateTime'][:10] == today :
                               print(event['summary'])
                               print()
                               GCal_today.append(event)
                       except:
                           if event['originalStartTime']['date'][:10] == today :
                               print(event['summary'])
                               print()
                               GCal_today.append(event)
           
           page_token = events.get('nextPageToken')
           if not page_token:
               break

       
    print()
       #Takes GCal Event and adds it to Notion DB
       
       #Takes all tasks for today from Notion and stores it in Notion_today
    Notion_tasks_today = []
    Notion_tasks_ID = []
    Notion_today = notion.databases.query(
           **{
            "database_id": database_id,
            "filter": {
                "and": [
                        {
                            "property": dateProperty, 
                            "date": {
                                "equals": today
                            }
                        }
                    ]   
                    }
    
            }
       )
    id_id = {}
    #Takes all Notion tasks and checks if they have anything in the GCal_ID property
    for Action_index, Action_Item in enumerate(Notion_today['results']):
        Action_Sub = Action_Item['properties']['GCal_ID']['rich_text']
        Notion_tasks_ID.append(Action_Sub)

    #Takes only the 'plain_text' values
    for list_index, list_item in enumerate(Notion_tasks_ID):
        
        if list_item != []:
            Notion_tasks_ID[list_index] = list_item[0]['plain_text']
            
            for ID_Guess in Notion_today['results']:
                
                if  ID_Guess['properties']['GCal_ID']['rich_text'] != []:
                    
                    if  ID_Guess['properties']['GCal_ID']['rich_text'][0]['plain_text'] == list_item[0]['plain_text']:
                        id_id[Notion_tasks_ID[list_index]] = ID_Guess['id']
        else:
            
            Notion_tasks_ID[list_index] = None
            
            
    while None in Notion_tasks_ID:
        
        Notion_tasks_ID.remove(None)
        
        
    #Prints the different daily tasks
    for Action_index, Action_Item in enumerate(Notion_today['results']):
        
           Action_Sub = Action_Item['properties'][nameProperty]['title'][0]['text']['content']

           Notion_tasks_today.append(Action_Sub)
           
    #Attach GCal_ID to Notion_Page_ID

    
    
    #Add GCal event to Notion
    for GCal_Event in GCal_today:
        
        #Check if the event name is already on Notion_today
        if GCal_Event['id'] not in Notion_tasks_ID :

            #Add the page
            try:
                new_page = notion.pages.create(
                            **{
                                "parent": {
                                    "database_id": database_id,
                                },

                                "properties": {
                                    'GCal_ID': {
                                        'type':'rich_text',
                                        'rich_text': [ {
                                            'id':'_}uo',
                                            'type':'text',
                                            'text': {
                                                'content': str(GCal_Event['id'])
                                                }
                                            } ]
                                        },
                                    
                                    nameProperty: {
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
                                    dateProperty: {
                                        "type": 'date',
                                        'date': {
                                            'start': GCal_Event['start']['dateTime'][:19],
                                            'end': GCal_Event['end']['dateTime'][:19], 
                                        }
                                    }
                                },
                            },
                        )
            except:
                new_page = notion.pages.create(
                            **{
                                "parent": {
                                    "database_id": database_id,
                                },
                                "properties": {
                                    'GCal_ID': {
                                        'type':'rich_text',
                                        'rich_text': [ {
                                            'id':'_}uo',
                                            'type':'text',
                                            'text': {
                                                'content': str(GCal_Event['id'])
                                                }
                                            } ]
                                        },
                                    nameProperty: {
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
                                    dateProperty: {
                                        "type": 'date',
                                        'date': {
                                            'start': GCal_Event['start']['date'],
                                            'end': None, 
                                        }
                                    }
                                },
                            },
                        )
        
        else:
            try:
                updated_page = notion.pages.update(
                                **{
                                    "page_id": id_id[GCal_Event['id']], 
                                    "properties": {
                                        'GCal_ID': {
                                        'type':'rich_text',
                                        'rich_text': [ {
                                            'id':'_}uo',
                                            'type':'text',
                                            'text': {
                                                'content': str(GCal_Event['id'])
                                                }
                                            } ]
                                        },
                                        nameProperty: {
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
                                        dateProperty: {
                                            "type": 'date',
                                            'date': {
                                                'start': GCal_Event['start']['date'],
                                                'end': None, 
                                                }
                                            }
                                        }
                                    }
                                )
            except:
                updated_page = notion.pages.update(
                                **{
                                    "page_id": id_id[GCal_Event['id']], 
                                    "properties": {
                                        'GCal_ID': {
                                        'type':'rich_text',
                                        'rich_text': [ {
                                            'id':'_}uo',
                                            'type':'text',
                                            'text': {
                                                'content': str(GCal_Event['id'])
                                                }
                                            } ]
                                        },
                                        nameProperty: {
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
                                        dateProperty: {
                                            "type": 'date',
                                            'date': {
                                                'start': GCal_Event['start']['dateTime'][:19],
                                                'end': GCal_Event['end']['dateTime'][:19], 
                                                }
                                            }
                                        }
                                    }
                                )
                
                
print('Sync done.')
