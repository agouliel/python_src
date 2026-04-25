import streamlit as st
import pandas as pd
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), '..', 'google_api', 'expenses.db')

st.title('Expenses')

with sqlite3.connect(db_path) as conn:
    df = pd.read_sql('SELECT * FROM expenses', conn)

if df.empty:
    st.info('No data found.')
    st.stop()

df['date_start'] = pd.to_datetime(df['date_start'])
df['year'] = df['date_start'].dt.year
df['month'] = df['date_start'].dt.month

years = sorted(df['year'].unique(), reverse=True)
selected_year = st.sidebar.selectbox('Year', years)

filtered = df[df['year'] == selected_year]

pivot = (
    filtered.groupby(['hashtag', 'month'])['amount']
    .sum()
    .unstack(level='month')
    .fillna(0)
)

month_names = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
               7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
month_num = {v: k for k, v in month_names.items()}
pivot.columns = [month_names[m] for m in pivot.columns]
pivot.index.name = None
pivot = pivot.sort_index()
pivot['Total'] = pivot.sum(axis=1)

totals_row = pivot.sum(axis=0).rename('Total')
pivot = pd.concat([pivot, totals_row.to_frame().T])

def build_tooltip(hashtag, col):
    mask = pd.Series([True] * len(filtered), index=filtered.index)
    if hashtag != 'Total':
        mask &= filtered['hashtag'] == hashtag
    if col != 'Total':
        mask &= filtered['month'] == month_num[col]
    items = filtered[mask].sort_values('date_start')
    if items.empty:
        return ''
    return '\n'.join(
        f"{row['date_start'].strftime('%d')}: {row['summary']} ({row['amount']:,.2f})"
        for _, row in items.iterrows()
    )

css = """
<style>
.exp-table { border-collapse: collapse; width: 100%; font-size: 0.9em; }
.exp-table th, .exp-table td {
    border: 1px solid #444; padding: 6px 10px; text-align: right;
}
.exp-table th:first-child, .exp-table td:first-child { text-align: left; }
.exp-table thead th { background: #4a4a6a; color: #fff; font-weight: 600; letter-spacing: 0.05em; }
.exp-table tbody tr:last-child td { font-weight: bold; border-top: 2px solid #888; }
.exp-table td:last-child { font-weight: bold; }
.tip { position: relative; cursor: help; }
.tip .tip-text {
    display: none; position: absolute; bottom: 110%; left: 50%;
    transform: translateX(-50%);
    background: #2a2a3e; color: #eee; border: 1px solid #666;
    padding: 6px 10px; border-radius: 6px;
    white-space: pre; font-size: 0.85em; z-index: 999;
    pointer-events: none; min-width: 200px;
}
.tip:hover .tip-text { display: block; }
</style>
"""

def fmt(v):
    return f'{v:,.2f}' if v != 0 else '—'

rows_html = ''
for idx in pivot.index:
    cells = f'<td>{idx}</td>'
    for col in pivot.columns:
        val = pivot.loc[idx, col]
        tip = build_tooltip(idx, col) if idx != 'Total' and col != 'Total' else ''
        if tip:
            cells += f'<td class="tip">{fmt(val)}<span class="tip-text">{tip}</span></td>'
        else:
            cells += f'<td>{fmt(val)}</td>'
    rows_html += f'<tr>{cells}</tr>'

header = '<tr><th></th>' + ''.join(f'<th>{c}</th>' for c in pivot.columns) + '</tr>'
html = f'{css}<table class="exp-table"><thead>{header}</thead><tbody>{rows_html}</tbody></table>'

st.markdown(html, unsafe_allow_html=True)
