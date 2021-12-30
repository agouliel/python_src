# https://twitter.com/reuvenmlerner/status/1476216683878666244

# The first line scrapes the Wikipedia page for the Apollo program,
# putting all HTML tables into data frames.
# The missions are in the third table, aka index 2.
# The second line turns lines containing date ranges into single (launch) dates,
# also removing commas and hyphens.

import pandas as pd

df = pd.read_html('https://en.wikipedia.org/wiki/Apollo_program')[2]
df['Date'] = pd.to_datetime(df['Date'].str.replace('(–.+)?,', '', regex=True))
df = df.set_index(‘Date')
