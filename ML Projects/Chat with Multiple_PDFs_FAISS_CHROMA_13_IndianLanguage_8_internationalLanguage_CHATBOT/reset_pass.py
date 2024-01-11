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
        if authenticator.reset_password(st.session_state["username"], 'Reset password'):
            st.success('New password changed')
    if not st.session_state["authentication_status"]:
        st.subheader('You need to login to change the password')

    with open('./config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)


if __name__ == '__main__':
    main()