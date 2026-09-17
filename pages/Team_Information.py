import streamlit as st

st.sidebar.page_link('Log_In.py')
st.sidebar.page_link('pages/League_Standings.py')
if (st.user.email in st.secrets['admin_emails']): st.sidebar.page_link('pages/Update_Spreadsheet.py')

teams = st.session_state.sheet.worksheet('Team Information')
    
if (st.user.email not in teams.col_values(1)[1:]):
    st.header('Create Your Team!')
    # TODO
else:
    team = teams.col_values(1).index(st.user.email) + 1

    st.header(teams.cell(team, 2).value)
    st.subheader('Survivors')
    st.write(teams.cell(team, 3).value.replace(' | ', '\n\n'))
    # TODO Add other survivor info? Images?
    st.subheader(f'Total Points: {teams.cell(team, 4).numeric_value}')
    st.write('Breakdown:')
    # st.caption(teams.col_values.replace(' | ', '\n\n'))