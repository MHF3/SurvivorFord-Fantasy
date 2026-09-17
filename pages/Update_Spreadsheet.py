import streamlit as st

st.sidebar.page_link('Log_In.py')
st.sidebar.page_link('pages/Team_Information.py')
st.sidebar.page_link('pages/League_Standings.py')

survivors = st.session_state.sheet.worksheet('Survivor Information')

st.header('Add New Episode Scores')

st.text_input('Row Title', key = 'title', placeholder = 'Ex. Episode 1', persist_state = 'session')

def confirmed() -> None:
    new_row = [None for _ in range(survivors.col_count)]
    new_row[0] = st.session_state.title
    
    
    # survivors.append_row(new_row)
    
    st.session_state.title = None
    # st.rerun()
    st.write(new_row)

@st.dialog('Confirm New Data')
def confirm() -> None:
    st.write('You are adding new data to the spreadsheet. It is important that this data is complete and accurate. If you are confident the data is correct, click Confirm; otherwise, click out of this dialog and verify the accuracy.')
    st.button('Confirm', on_click = confirmed)

if st.button('Add Data'): confirm()