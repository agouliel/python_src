import datetime, sys, sqlite3, os
from gcal import service
from collections import defaultdict

# sample: 2021-11-29T13:31:42.108271Z - 'Z' indicates UTC time
now = datetime.datetime.utcnow().isoformat() + 'Z'
# a warning appears that says to use the below:
#now = datetime.datetime.now(datetime.UTC).isoformat() + 'Z'
# but then we get a "Bad Request" error

if len(sys.argv) > 1:
      month_start = sys.argv[1] + 'T00:00:00.000000Z'
else:
      month_start = datetime.datetime.today().date().replace(day=1).isoformat() + 'T00:00:00.000000Z'

if len(sys.argv) > 2:
      month_end = sys.argv[2] + 'T00:00:00.000000Z'
else:
      month_end = now

events_result = service.events().list(calendarId='primary',
                                        timeMin=month_start,
                                        timeMax=month_end,
                                        #maxResults=10,
                                        singleEvents=True,
                                        orderBy='startTime').execute()

events = events_result.get('items', [])

totals_by_hashtag = defaultdict(float)
grand_total = 0

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
            grand_total += amount

sorted_dict = dict(sorted(totals_by_hashtag.items()))
for k in sorted_dict:
     print(k[1:]+'\t'+str(sorted_dict[k]))
print('Total:', grand_total)

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'expenses.db')
date_from = month_start[:10]
date_to = month_end[:10]
with sqlite3.connect(db_path) as conn:
    conn.execute('''CREATE TABLE IF NOT EXISTS expense_totals (
        date_from TEXT,
        date_to TEXT,
        hashtag TEXT,
        total REAL,
        PRIMARY KEY (date_from, date_to, hashtag)
    )''')
    conn.executemany(
        'INSERT OR REPLACE INTO expense_totals VALUES (?, ?, ?, ?)',
        [(date_from, date_to, k[1:], v) for k, v in sorted_dict.items()]
    )
    conn.commit()
print(f'Saved to {db_path}')