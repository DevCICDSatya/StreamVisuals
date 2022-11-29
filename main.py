import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
from vega_datasets import data
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
# st.image("data/ups.png",width=1200)
st.markdown("""
<style>
div[data-testid="metric-container"] {
   background-color: #9ef0f0;
   border: 1px solid rgba(28, 131, 225, 0.1);
   padding: 5% 5% 5% 10%;
   border-radius: 5px;
   color: rgb(30, 103, 119);
   overflow-wrap: break-word;
}

/* breakline for metric text         */
div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
   overflow-wrap: break-word;
   white-space: break-spaces;
   color: red;
}
</style>
"""
            , unsafe_allow_html=True)
df = pd.read_csv('data.csv',sep=",",encoding='windows-1252')
total = []
for i in range(len(df['QUANTITYORDERED'])):
    a = (df['QUANTITYORDERED'][i] * df['PRICEEACH'][i])
    total.append(a)
df['Total_Price'] = total
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${round(df['Total_Price'].sum(),2)}", "9%")
col2.metric("Countries", "23", "6")
col3.metric("P/L Ratio", "86%", "4%")

total_categeory_sales = df.groupby(['PRODUCTLINE'])['PRODUCTLINE'].count().reset_index(name="count")

a,b = st.columns(2)
with a:
    st.header('Total sales by category')
    st.markdown('')
    st.bar_chart(total_categeory_sales,x='PRODUCTLINE', y='count')


year_sales = df.groupby(['YEAR_ID'])['YEAR_ID'].count().reset_index(name="count")
with b:
    fig = px.pie(year_sales, values='count', names='YEAR_ID', title='Year wise Sales',
                 hover_data=['count'])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(legend=dict(title_font_family="Open Sans", font=dict(size=24)), title=dict(
        x=0.5,
        y=0.95,
        font=dict(
            size=36,
            color='#262730'
        )
    ))
    st.plotly_chart(fig,use_container_width=True)

x,y  = st.columns(2)
with x:
    countries = df.groupby(['COUNTRY'])['COUNTRY'].count().reset_index(name="count")
    fig1 = go.Figure(data=[go.Pie(labels=countries['COUNTRY'], values=countries['count'], hole=.3)])
    st.plotly_chart(fig1,use_container_width=True)
