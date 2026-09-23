import gspread
import streamlit as st

st.sidebar.page_link('Log_In.py')
st.sidebar.page_link('pages/Vote_Prediction.py')
st.sidebar.page_link('pages/League_Standings.py')
if (st.user.email in st.secrets['admin_emails']):
    st.sidebar.page_link('pages/Update_Spreadsheet.py')
    st.sidebar.page_link('pages/Toggle_Lock.py')

if ('sheet' not in st.session_state):
    bot = gspread.service_account_from_dict(dict(st.secrets['service_account']))
    st.session_state.sheet = bot.open_by_url(st.secrets['spreadsheet'])

teams = st.session_state.sheet.worksheet('Team Information')

if ('team_row' not in st.session_state):
    try: st.session_state.team_row = teams.col_values(1).index(st.user.email) + 1
    except ValueError: st.session_state.team_row = -1

if (st.session_state.team_row == -1): st.header('Sign up through the link in the GroupMe to create your team!')
else:
    if ('team_name' not in st.session_state): st.session_state.team_name = teams.cell(st.session_state.team_row, 2).value
    if ('team_survivors' not in st.session_state): st.session_state.team_survivors = teams.cell(st.session_state.team_row, 3).value.replace(' | ', '\n\n')
    if ('team_points' not in st.session_state): st.session_state.team_points = teams.cell(st.session_state.team_row, 4).numeric_value
    if ('team_breakdown' not in st.session_state):
        if (teams.cell(st.session_state.team_row, 5).value != None): st.session_state.team_breakdown = teams.cell(st.session_state.team_row, 5).value.replace(' | ', '\n\n')

    st.header(st.session_state.team_name)
    st.subheader('Survivors')
    st.write(st.session_state.team_survivors)
    # TODO Add other survivor info? Images?
    st.subheader(f'Total Points: {st.session_state.team_points}')
    if ('team_breakdown' in st.session_state):
        with st.expander('Point Breakdown'):
            st.caption(st.session_state.team_breakdown)