import requests
import streamlit as st

API_KEY = st.secrets["jsonbin_api_key"]
headers = {
    "X-Master-Key": API_KEY,
    "Content-Type": "application/json"
}


def load_data(data_file):
    res = requests.get(data_file, headers=headers)
    return res.json()["record"]


def save_data(data, data_file):
    res = requests.put(data_file, headers=headers, json=data)
    return res.json()
