import streamlit as st
import streamlit.auth as auth
import requests

authorized_password = st.secrets["my_password"]
api_key = st.secrets["api_key"]
device_id = st.secrets["device_id"]
model = st.secrets["model"]

# Set up authentication

if not auth.is_authenticated():
    password = st.text_input("Enter password", type="password")
    if password == authorized_password:
        auth.authenticate()

# Display the protected content
if auth.is_authenticated():
    url = f'https://developer-api.govee.com/v1/devices/control'

    headers = {
        'Govee-API-Key': api_key,
        'Content-Type': 'application/json'
    }

    content = {
        'device': device_id,
        'model': model,
        'cmd': {
            'name': 'turn',
            'value': 'on'
        }
    }

    response = requests.put(url, headers=headers, json=content)

    if response.status_code == 200:
        st.write('You turned my light on!')
    else:
        print(f'Error turning on device: {response.text}')
