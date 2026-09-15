import streamlit as st
from streamlit_gsheets import GSheetsConnection

if not st.user.is_logged_in: st.header('Log In Required!')
else:
    # FIXME
    st.title('Test')

    spreadsheet = st.connection('gsheets', type = GSheetsConnection)
    df = spreadsheet.read(worksheet = 'Episodic Events', ttl = 0)

    st.dataframe(df)