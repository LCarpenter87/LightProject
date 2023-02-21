import streamlit as st
import requests

authorized_password = st.secrets["my_password"]
api_key = st.secrets["api_key"]
device_id = st.secrets["device_id"]
model = st.secrets["model"]

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True











# Display the protected content
if check_password():
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
