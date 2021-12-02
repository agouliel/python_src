import datetime, sys
from gcal import service

# sample: 2021-11-29T13:31:42.108271Z - 'Z' indicates UTC time
now = datetime.datetime.utcnow().isoformat() + 'Z'

if len(sys.argv) > 1:
      month_start = sys.argv[1] + 'T00:00:00.000000Z'
else:
      month_start = datetime.datetime.today().date().replace(day=1).isoformat() + 'T00:00:00.000000Z'

events_result = service.events().list(calendarId='primary',
                                        timeMin=month_start,
                                        timeMax=now,
                                        #maxResults=10, 
                                        singleEvents=True,
                                        orderBy='startTime').execute()

events = events_result.get('items', [])

mydict = {}

for event in events:
      if event['summary'].startswith('*'): # family expenses start with asterisk
        start = event['start'].get('dateTime', event['start'].get('date'))
        startdt = start[:10]
        event_summary = event['summary'][2:] # remove asterisk

        # extract numbers - this will fail if the numbers are in the x+y format
        summary_numbers = [int(s) for s in event_summary.split() if s.isdigit()]
        try:
          event_amnt = summary_numbers[0]
        except:
          event_amnt = 0

        if startdt in mydict: # this date already exists, so add the new data
          mydict[startdt] = [mydict[startdt][0]+event_amnt, mydict[startdt][1]+' + '+event_summary]
        else:
          mydict[startdt] = [event_amnt, event_summary]

# add missing dates
# first create a set with every distinct month, and then append days
# this isn't entirely correct, because it assumes that all months have 31 days
myset = set()
for i in mydict:
      myset.add(i[:8])

for j in myset:
      for k in range(1, 32):
        mydt = j + f'{k:02}'
        if mydt not in mydict:
          mydict[mydt] = []

mysorteddict = {k: v for k, v in sorted(mydict.items(), key=lambda item: item[0])}

for mykey in mysorteddict:
      if mysorteddict[mykey]:
        print(mykey, mysorteddict[mykey][1], str(mysorteddict[mykey][0]), sep=';')
      else:
        print(mykey+';'+';')
