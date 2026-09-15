import streamlit as st

if not st.user.is_logged_in: st.header('Log In Required!')
else:
    # FIXME
    st.title('Test')

    data = st.session_state.sheet.worksheet('Episodic Events')

    st.write(data)