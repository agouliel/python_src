import datetime, sys, sqlite3, os
import psycopg2
from gcal import service as gcal_service
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

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'expenses.db')
with sqlite3.connect(db_path) as conn:
    conn.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id TEXT,
        date_start TEXT,
        hashtag TEXT,
        summary TEXT,
        amount REAL,
        PRIMARY KEY (id)
    )''')

events_result = gcal_service.events().list(calendarId='primary',
                                        timeMin=month_start,
                                        timeMax=month_end,
                                        #maxResults=10,
                                        singleEvents=True,
                                        orderBy='startTime').execute()

events = events_result.get('items', [])

totals_by_hashtag = defaultdict(float)
grand_total = 0

events_with_expenses = []

for event in events:
    #{'kind': 'calendar#event', 'etag': '"3540035831135966"', 'id': '4k71ki9tgdh0ng4eqb0huspc07', 'status': 'confirmed',
    # 'htmlLink': 'https://www.google.com/calendar/event?eid=NGs3MWtpOXRnZGgwbmc0ZXFiMGh1c3BjMDcgYWdvdWxpZWxAbQ',
    # 'created': '2026-01-29T09:39:04.000Z', 'updated': '2026-02-02T07:38:35.567Z', 'summary': '30 cohen #drinks',
    # 'creator': {'email': 'agouliel@gmail.com', 'self': True},
    # 'organizer': {'email': 'agouliel@gmail.com', 'self': True},
    # 'start': {'dateTime': '2026-01-30T09:00:00+02:00', 'timeZone': 'Europe/Athens'},
    # 'end': {'dateTime': '2026-01-30T10:00:00+02:00', 'timeZone': 'Europe/Athens'},
    # 'iCalUID': '4k71ki9tgdh0ng4eqb0huspc07@google.com', 'sequence': 0, 'reminders': {'useDefault': True},
    # 'eventType': 'default'
    #}
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

            event_with_expense = (
                event.get('id'),
                event['start']['dateTime'][:10],
                hashtag[1:],
                ' '.join(parts[1:-1]), # summary
                amount,
            )
            events_with_expenses.append(event_with_expense)

sorted_dict = dict(sorted(totals_by_hashtag.items()))
for k in sorted_dict:
     print(k[1:]+'\t'+str(sorted_dict[k]))
print('Total:', grand_total)

with sqlite3.connect(db_path) as conn:
    conn.executemany('INSERT OR REPLACE INTO expenses VALUES (?, ?, ?, ?, ?)', events_with_expenses)
    conn.commit()
print(f'Saved to {db_path}')

pg_host = os.environ.get('PGHOST')
if pg_host:
    pg_conn = psycopg2.connect(
        host=pg_host,
        port=os.environ.get('PGPORT', 5432),
        dbname=os.environ.get('PGDATABASE'),
        user=os.environ.get('PGUSER'),
        password=os.environ.get('PGPASSWORD'),
    )
with pg_conn:
    with pg_conn.cursor() as cur:
        cur.executemany(
            '''INSERT INTO expenses (id, date_start, hashtag, summary, amount, url) VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    date_start = EXCLUDED.date_start, hashtag = EXCLUDED.hashtag,
                    summary = EXCLUDED.summary, amount = EXCLUDED.amount, url = EXCLUDED.url''',
            events_with_expenses
        )
