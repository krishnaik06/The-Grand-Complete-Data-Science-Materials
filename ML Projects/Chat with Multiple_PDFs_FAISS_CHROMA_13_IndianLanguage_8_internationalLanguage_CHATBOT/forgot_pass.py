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

    username_forgot_pw, email, random_password = authenticator.forgot_password('Forgot password')
    if username_forgot_pw:
        st.success(f'New random password is : {random_password}.. Change it in next login')
        # Random password to be transferred to user securely
    elif username_forgot_pw == False:
        st.error('Username not found')


    with open('./config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

if __name__ == '__main__':
    main()