import streamlit as st
import requests, json
from web3 import Web3
import pandas as pd

endpoint = st.sidebar.selectbox("Endpoints", ["Assets","Events","Rarity"])
st.header(f"OpenSea Testnets NFT API explorer -- {endpoint}")


## RETRIEVING ASSETS ##
if endpoint == "Assets" :
    st.sidebar.subheader("Filters")
    collection = st.sidebar.text_input("Collection")
    owner = st.sidebar.text_input("Owner")
    params = {}
    if collection:
        params['collection'] = collection
    if owner:
        params['owner'] = owner
    r = requests.get("https://testnets-api.opensea.io/api/v1/assets", params = params)
   
    assets = r.json()['assets']

    for asset in assets:
        st.write("collection ",asset["collection"]['name'])
        st.write(asset['name']," - token ID ",asset['token_id'])
        if asset['image_url']: 
            st.image(asset['image_url'])

    st.write(assets)
    

## RETRIEVING EVENTS ##
if endpoint == "Events":
    collection = st.sidebar.text_input("Collection")
    asset_contract_address = st.sidebar.text_input("Contract address")
    token_id = st.sidebar.text_input("Token ID")
    event_type = st.sidebar.selectbox("Event Type", ['bid_entered', 'cancelled', 'bid_withdrawn', 'transfer', 'approve'])
    params = {}

    if collection:
        params['collection_slug'] = collection
    if asset_contract_address:
        params['asset_contract_address'] = asset_contract_address
    if token_id:
        params['token_id'] = token_id
    if event_type:
        params['event_type'] = event_type
    
    r = requests.get('https://testnets-api.opensea.io/api/v1/events', params=params)

    events = r.json()

    event_list = []
    for event in events['asset_events']:
        bidder = ""
        bid_amount = 0
        if event_type == "bid_entered":
            if event["bid_amount"]:
                ## convert from wei to eth
                bid_amount = Web3.fromWei(int(event['bid_amount']), 'ether')
            if event['from_account']['user']:
                bidder = event['from_account']['user']['username']
            else:
                bidder = event['from_account']['address']
        event_list.append([event['created_date'], bidder, float(bid_amount), event['asset']['collection']['name'], event['asset']['token_id']])
    
    df = pd.DataFrame(event_list, columns = ['time', 'bidder', 'bid_amount', 'collection', 'token_id'])

    st.write(df)
    ## RAW JSON
    st.write(events)
