import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

if "access_token" not in st.session_state:
    st.session_state["access_token"] = None
if "refresh_token" not in st.session_state:
    st.session_state["refresh_token"] = None


def show_auth_page():
    st.title("Sign-In Service")

    st.header("Sign up")

    with st.form("signup_form"):
        signup_username = st.text_input("Username", key="signup_username")
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_password")
        signup_submitted = st.form_submit_button("Sign up")

    if signup_submitted:
        response = requests.post(
            f"{API_URL}/signup",
            json={
                "username": signup_username,
                "email": signup_email,
                "password": signup_password,
            },
        )
        if response.status_code == 201:
            st.success(f"Account created for {response.json()['username']}")
        else:
            st.error(f"Signup failed: {response.json().get('detail', response.text)}")

    st.header("Log in")

    with st.form("login_form"):
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        login_submitted = st.form_submit_button("Log in")

    if login_submitted:
        response = requests.post(
            f"{API_URL}/login",
            data={
                "username": login_username,
                "password": login_password,
            },
        )
        if response.status_code == 200:
            tokens = response.json()
            st.session_state["access_token"] = tokens["access_token"]
            st.session_state["refresh_token"] = tokens["refresh_token"]
            st.rerun()
        else:
            st.error(f"Login failed: {response.json().get('detail', response.text)}")


def show_me_page():
    st.title("Welcome")

    response = requests.get(
        f"{API_URL}/me",
        headers={"Authorization": f"Bearer {st.session_state['access_token']}"},
    )

    if response.status_code == 200:
        user = response.json()
        st.write(f"**Username:** {user['username']}")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Account created:** {user['created_at']}")
    else:
        st.error("Session expired or invalid. Please log in again.")

    if st.button("Log out"):
        st.session_state["access_token"] = None
        st.session_state["refresh_token"] = None
        st.rerun()


if st.session_state["access_token"]:
    show_me_page()
else:
    show_auth_page()