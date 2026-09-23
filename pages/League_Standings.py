import gspread
import streamlit as st

st.sidebar.page_link('Log_In.py')
st.sidebar.page_link('pages/Team_Information.py')
st.sidebar.page_link('pages/Vote_Prediction.py')
if (st.user.email in st.secrets['admin_emails']):
    st.sidebar.page_link('pages/Update_Spreadsheet.py')
    st.sidebar.page_link('pages/Toggle_Lock.py')

if ('sheet' not in st.session_state):
    bot = gspread.service_account_from_dict(dict(st.secrets['service_account']))
    st.session_state.sheet = bot.open_by_url(st.secrets['spreadsheet'])

if ('team_scores' not in st.session_state):
    teams_data = st.session_state.sheet.worksheet('Team Information').get_all_values()
    team_scores = {teams_data[row][1]: int(teams_data[row][3]) for row in range(1, len(teams_data))}
    st.session_state.team_scores = {team: score for team, score in sorted(team_scores.items(), key = lambda item: item[1], reverse = True)}

st.header('Standings')

place = 0
for team, score in st.session_state.team_scores.items():
    place += 1
    st.write(f'**{place}**:   {team} - {score}')