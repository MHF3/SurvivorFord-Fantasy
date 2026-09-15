import streamlit as st

def login(): st.button('Log In', on_click = st.login, icon = ':material/login:')

if st.user.is_logged_in:
    st.header(f'Hey {st.user.name}!')
    st.subheader("Try to become Haverford's Fantastical Survivor!")
    st.button('Log Out', on_click = st.logout, icon = ':material/logout:')
else:
    st.title('Log In Using Your School Email')
    login()