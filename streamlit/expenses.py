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

row_height = 35
header_height = 38
height = header_height + row_height * len(pivot) + 3

col_config = {col: st.column_config.NumberColumn(format="%.2f") for col in pivot.columns}

col_table, col_detail = st.columns([3, 1])

with col_table:
    event = st.dataframe(
        pivot,
        use_container_width=True,
        height=height,
        column_config=col_config,
        on_select="rerun",
        selection_mode="single-cell",
    )

with col_detail:
    sel = event.selection
    cells = sel.get("cells", []) if isinstance(sel, dict) else getattr(sel, "cells", [])
    if cells:
        hashtag = pivot.index[cells[0][0]]
        month_col = cells[0][1]
        if hashtag == 'Total' or month_col == 'Total':
            st.info('No details for totals.')
        elif month_col not in month_num:
            st.info('No details available.')
        else:
            items = filtered[
                (filtered['hashtag'] == hashtag) &
                (filtered['month'] == month_num[month_col])
            ].sort_values('date_start')
            st.subheader(f"{hashtag} · {month_col}")
            if items.empty:
                st.write('No expenses.')
            else:
                for _, row in items.iterrows():
                    st.write(f"**{row['date_start'].strftime('%d')}** {row['summary']} — {row['amount']:,.2f}")
    else:
        st.caption('Click a cell to see details.')

