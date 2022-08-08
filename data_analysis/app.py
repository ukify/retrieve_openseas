from turtle import width
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib_venn import venn2

@st.cache
def get_data():
    path = 'fourCollections.csv'
    df = pd.read_csv(path, dtype={'collection_slug': 'str', 'asset_id': 'int', 'asset_name': 'str', 'owner_username': 'str', 'owner_address': 'str', 'event_type': 'str'})
    # Clean Data
    df.drop('Unnamed: 0.1', axis=1, inplace=True)
    df.drop('asset_id', axis=1, inplace=True)
    df.drop('Unnamed: 0', axis=1, inplace=True)
    df.drop('collection_slug', axis=1,inplace=True)
    df.drop('asset_contract_date', axis=1, inplace=True)
    df['event_timestamp'] = pd.to_datetime(df['event_timestamp'])
    df.drop_duplicates(keep='first')

    df.set_index(df['event_timestamp'], inplace=True)
    return df
df = get_data()

@st.cache
def collection_name():
    collection_name = {
        'Azuki': 'Azuki',
        'Bored Ape Yacht Club': 'Bored Ape Yacht Club',
        'mfers': 'mfers',
        'Crypto Coven': 'Crypto Coven'
    }
    return collection_name
collection_name = collection_name()

@st.cache
def event_name():
    event_name = {
        'created': 'created',
        'successful': 'successful',
        'cancelled': 'cancelled',
        'bid_entered': 'bid_entered',
        'bid_withdrawnn': 'bid_withdrawn',
        'transfer': 'transfer',
        'approve': 'approve',
        'offer_entered': 'offer_entered'
    }
    return event_name
event_name = event_name()

# Filter
df_filtered = pd.DataFrame()
df_filtered['Collection Name'] = df['collection_name']
df_filtered['Asset Name'] = df['asset_name']
df_filtered['Username'] = df['owner_username']
df_filtered['Owner_Address'] = df['owner_address']
df_filtered['Event Type'] = df['event_type']

# App Body
st.title('NFT Collection Data')

with st.form("Filters"):
    with st.sidebar:
        st.title('Collection Filter')

        event_filter = st.multiselect('Enter Event Name', event_name)
        df_filtered = df_filtered[(df_filtered['Event Type'].isin(event_filter))]

        collection_filter = st.multiselect('Enter Collection Name', collection_name)
        df_filtered = df_filtered[(df_filtered['Collection Name'].isin(collection_filter))]

        start = st.date_input('Select Start Date').strftime('%Y-%m-%dT00:00:00')
        end = st.date_input('Select End Date').strftime('%Y-%m-%dT00:00:00')

        df_filtered = df_filtered.loc[start:end]

        submitted = st.form_submit_button("Submit")

df_graph = df_filtered.resample('D').apply({'Owner_Address':'count'})

fig = plt.figure(figsize=(1, 5))

plt.plot(df_graph)

st.plotly_chart(fig, use_container_width=True)

st.write(df_filtered)

