import streamlit as st

st.sidebar.page_link('Log_In.py')
st.sidebar.page_link('pages/League_Standings.py')
if (st.user.email in st.secrets['admin_emails']): st.sidebar.page_link('pages/Update_Spreadsheet.py')

teams = st.session_state.sheet.worksheet('Team Information')
    
if (st.user.email not in teams.col_values(1)[1:]):
    st.header('Create Your Team!')
    # TODO
else:
    team = teams.col_values(1).index(st.user.email)

    st.header(teams.col_values(2)[team])
    st.subheader('Survivors')
    st.write(teams.col_values(3)[team].replace(' | ', '\n\n'))
    # TODO Add other survivor info? Images?
    st.subheader(f'Total Points: {teams.col_values(4)[team]}')
    st.write('Breakdown:')
    st.caption('test point gain 1\n\ntest point gain 2')