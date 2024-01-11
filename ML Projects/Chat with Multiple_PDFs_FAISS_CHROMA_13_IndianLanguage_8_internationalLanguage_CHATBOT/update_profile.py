import yaml
import streamlit as st
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader

def main():
    with open('./config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    if st.session_state["authentication_status"]:
        if authenticator.update_user_details(st.session_state["username"], 'Update user details'):
            st.success('Entries updated successfully')

    if not st.session_state["authentication_status"]:
        st.subheader('You need to login to update the profile')

    with open('./config.yaml', 'a') as file:
        yaml.dump(config, file, default_flow_style=False)

if __name__ == '__main__':
    main()