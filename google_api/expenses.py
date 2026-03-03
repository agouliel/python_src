import datetime, sys
from gcal import service
from collections import defaultdict

# sample: 2021-11-29T13:31:42.108271Z - 'Z' indicates UTC time
now = datetime.datetime.utcnow().isoformat() + 'Z'
# a wanring appears that says to use the below, but then we get a "Bad Request" error
#now = datetime.datetime.now(datetime.UTC).isoformat() + 'Z'

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

totals_by_hashtag = defaultdict(float)

for event in events:
    parts = event.get("summary", "").split()
    
    # Check if we have enough parts and if the first part is numeric
    if parts:
        first_word = parts[0]
        
        # This check handles both integers and decimals
        if first_word.replace('.', '', 1).isdigit():
            amount = float(first_word)
            hashtag = parts[-1]
            totals_by_hashtag[hashtag] += amount

print(dict(totals_by_hashtag))