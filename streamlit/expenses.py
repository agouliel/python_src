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

df['month'] = pd.to_datetime(df['date_start']).dt.to_period('M').astype(str)

months = sorted(df['month'].unique(), reverse=True)
selected = st.selectbox('Month', months)

filtered = df[df['month'] == selected]

totals = filtered.groupby('hashtag', as_index=False)['amount'].sum().sort_values('hashtag')

#st.bar_chart(totals.set_index('hashtag')['amount'])

st.dataframe(totals.reset_index(drop=True), use_container_width=True)

grand_total = totals['amount'].sum()
st.metric('Total', f'{grand_total:,.2f}')
