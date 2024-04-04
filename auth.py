import streamlit as st
import streamlit_authenticator as stauth
import datetime
import re


def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        st.error('Invalid Email!')
        return False
    return True


def register():
    with st.form(key='register', clear_on_submit=True):
        st.subheader(':green[Register]')
        email = st.text_input('Email', placeholder='Enter Your Email')
        username = st.text_input(
            'Username', placeholder='Enter Your Username')
        password = st.text_input(
            'Password', type='password', placeholder='Enter Password')
        confirm_password = st.text_input(
            'Confirm Password', type='password', placeholder='Confirm Password')
        submit = st.form_submit_button('Register')

        # if email:
        #     if validate_email(email):

        if submit:
            if password != confirm_password:
                st.error('Passwords do not match')
            else:
                stauth.sign_up(email, password)


def login():
    with st.form(key='login', clear_on_submit=True):
        st.subheader(':green[Login]')
        email = st.text_input('Email', placeholder='Enter Your Email')
        password = st.text_input(
            'Password', type='password', placeholder='Enter Password')
        submit = st.form_submit_button('Login')

        if submit:
            stauth.sign_in(email, password)
