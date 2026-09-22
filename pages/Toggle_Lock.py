import streamlit as st

st.sidebar.page_link('Log_In.py')
st.sidebar.page_link('pages/Team_Information.py')
st.sidebar.page_link('pages/Vote_Prediction.py')
st.sidebar.page_link('pages/League_Standings.py')
if (st.user.email in st.secrets['admin_emails']): st.sidebar.page_link('pages/Update_Spreadsheet.py')

if ('locked' not in st.session_state): st.session_state.locked = bool(st.session_state.sheet.worksheet('Locked').cell(1, 1).numeric_value)

st.header('Lock/Unlock Team Changes')
st.write('---')

def lock() -> None:
    st.session_state.sheet.worksheet('Locked').update_cell(1, 1, 1)
    st.session_state.locked = True

def unlock() -> None:
    st.session_state.sheet.worksheet('Locked').update_cell(1, 1, 0)
    st.session_state.locked = False

column_label, column_button = st.columns(2, vertical_alignment = 'bottom')
if (st.session_state.locked):
    with column_label: st.subheader('Currently Locked')
    with column_button: st.button('', on_click = unlock, icon = ':material/lock_open:')
else:
    with column_label: st.subheader('Currently Unlocked')
    with column_button: st.button('', on_click = lock, icon = ':material/lock:')