import streamlit as st

st.sidebar.page_link('Log_In.py')
st.sidebar.page_link('pages/Team_Information.py')
st.sidebar.page_link('pages/League_Standings.py')

survivors = st.session_state.sheet.worksheet('Survivor Information')
scoring = st.session_state.sheet.worksheet('Scoring Information')

st.header('Add New Episode Scores')

if ('points' not in st.session_state): st.session_state.points = []
if ('survivor_list' not in st.session_state): st.session_state.survivor_list = [survivor for survivor in survivors.row_values(1)[1:]]
if ('action_list' not in st.session_state): st.session_state.action_list = [action for column in range(scoring.column_count) for action in scoring.col_values(column + 1)[1:]]

st.text_input('Row Title', key = 'title', placeholder = 'Ex. Episode 1', persist_state = 'session')

def add_points() -> None:
    st.session_state.points.append({st.session_state.survivor: st.session_state.action})
    st.session_state.survivor = None
    st.session_state.action = None

with st.container(border = True):
    column_l, column_r = st.columns(2)

    with column_l: st.selectbox('Survivor', st.session_state.survivor_list, None, key = 'survivor', placeholder = 'Who scored points', persist_state = 'session')
    with column_r: st.selectbox('Action', st.session_state.action_list, None, key = 'action', placeholder = 'What scored points', persist_state = 'session')

    if (st.session_state.survivor and st.session_state.action): st.button('Add Points', on_click = add_points)
    else: st.button('Add Points', disabled = True)

    with st.expander('Current Added Points'):
        for point in st.session_state.points: st.caption(f'{next(iter(point.keys()))}: {next(iter(point.values()))}')

def confirmed() -> None:
    new_row = [None for _ in range(survivors.col_count)]
    new_row[0] = st.session_state.title

    survivor_index = 0
    for name in st.session_state.survivor_list:
        survivor_index += 1
        survivor_column = survivor_index + 1
        survivor_points = []
        gained_points = 0

        for point in st.session_state.points:
            if (name == next(iter(point.keys()))):
                point_action = next(iter(point.values()))
                survivor_points.append(point_action)

                for column in range(1, scoring.column_count + 1):
                    value = 0
                    if (point_action in scoring.col_values(column)): value = int(scoring.col_values(column)[0])
                    gained_points += value
        
        if (survivor_points):
            new_row[survivor_index] = ' | '.join(survivor_points)

            curr_points = survivors.cell(3, survivor_column).numeric_value
            survivors.update_cell(3, survivor_column, curr_points + gained_points)

    survivors.append_row(new_row)
    
    st.session_state.title = None
    st.session_state.points = []
    st.rerun()

@st.dialog('Confirm New Data')
def confirm() -> None:
    st.write('You are adding new data to the spreadsheet. It is important that this data is complete and accurate. If you are confident the data is correct, click Confirm; otherwise, click out of this dialog and verify the accuracy.')
    st.button('Confirm', on_click = confirmed)

if (st.session_state.title and st.session_state.points): st.button('Append All Points', on_click = confirm)
else: st.button('Append All Points', disabled = True)