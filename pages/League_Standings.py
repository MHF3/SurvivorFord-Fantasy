import streamlit as st

st.sidebar.page_link('Log_In.py')
st.sidebar.page_link('pages/Team_Information.py')
if (st.user.email in st.secrets['admin_emails']): st.sidebar.page_link('pages/Update_Spreadsheet.py')

teams = st.session_state.sheet.worksheet('Team Information')

team_scores = {teams.col_values(2)[i + 1]: int(teams.col_values(4)[i + 1]) for i in range(len(teams.col_values(4)[1:]))}
sorted_team_scores = {team: score for team, score in sorted(team_scores.items(), key = lambda item: item[1], reverse = True)}

st.header('Standings')

place = 0
for team, score in sorted_team_scores.items():
    place += 1
    st.write(f'**{place}**:   {team} - {score}')