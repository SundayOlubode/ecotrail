import streamlit as st
import streamlit_authenticator as stauth
import datetime
import re
from database import get_user_by_email, get_user_by_username, register_user, login_user


def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        st.error('Invalid Email!')
        return False
    return True


def set_cookie_value(key, value):
    session_state = st.session_state
    session_state[key] = value


def get_cookie_value(key):
    session_state = st.session_state
    return session_state.get(key, None)


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
        st.form_submit_button('Register')

        if email:
            if validate_email(email):
                oldUser = get_user_by_email(email)
                if oldUser:
                    st.warning('User already exists! Please login.')
                    return
            else:
                st.warning('Please enter a valid email address')
        else:
            st.warning('Please enter an email address')
            return

        if username:
            oldUser = get_user_by_username(username)
            if oldUser:
                st.warning('Username already exists! Please choose another.')
                return
        else:
            st.warning('Please enter a username')
            return

        if not password:
            st.warning('Please enter a password')
            return
        if len(password) < 5:
            st.warning('Password must be at least 5 characters')
            return
        if password != confirm_password:
            st.warning('Passwords do not match!')
            return

        register_user(email, username, password)
        st.success('User registered successfully! Please login.')


def login():
    with st.form(key='login', clear_on_submit=True):
        st.subheader(':green[Login]')
        email = st.text_input('Email', placeholder='Enter Your Email')
        password = st.text_input(
            'Password', type='password', placeholder='Enter Password')
        submit = st.form_submit_button('Login')

        user = get_user_by_email(email)

        if not user:
            st.error('User does not exist. Please register.')
            return

        username = ''

        if email == user['email'] and password == user['password']:
            username = user['username']
            st.success("Logged in as {}".format(user['username']))
        else:
            st.error("Invalid credentials, Try Again!")

        if submit:
            set_cookie_value(email, username)
