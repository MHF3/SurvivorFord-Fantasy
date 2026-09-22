import gspread
import streamlit as st

if st.user.is_logged_in:
    st.sidebar.page_link('pages/Team_Information.py')
    st.sidebar.page_link('pages/Vote_Prediction.py')
    st.sidebar.page_link('pages/League_Standings.py')
    if (st.user.email in st.secrets['admin_emails']):
        st.sidebar.page_link('pages/Update_Spreadsheet.py')
        st.sidebar.page_link('pages/Toggle_Lock.py')

    if ('sheet' not in st.session_state):
        bot = gspread.service_account_from_dict(dict(st.secrets['service_account']))
        st.session_state.sheet = bot.open_by_url(st.secrets['spreadsheet'])

    st.header(f'Hey {st.user.name}!')
    st.subheader("Try to become Haverford's Fantastical Survivor!")
    st.button('Log Out', on_click = st.logout, icon = ':material/logout:')
else:
    st.title('Log In Using Your School Email')
    st.button('Log In', on_click = st.login, icon = ':material/login:')