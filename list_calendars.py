from cal_setup import get_calendar_service

def main():
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
       primary = "Primary" if calendar.get('primary') else ""
       #print("%s\t%s\t%s" % (summary, id, primary))
   return calendars

if __name__ == '__main__':
   main()