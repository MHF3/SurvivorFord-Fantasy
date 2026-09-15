import streamlit as st

if not st.user.is_logged_in: st.header('Log In Required!')
else:
    teams = st.session_state.sheet.worksheet('Team Information')
    
    if (st.user.email not in teams.col_values(1)[1:]):
        st.header('Create Your Team!')
        # TODO
    else:
        # team = data.in
        st.header(f'In Progres')