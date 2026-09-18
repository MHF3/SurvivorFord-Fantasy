import streamlit as st

st.sidebar.page_link('Log_In.py')
st.sidebar.page_link('pages/Team_Information.py')
st.sidebar.page_link('pages/League_Standings.py')

teams = st.session_state.sheet.worksheet('Team Information')
survivors = st.session_state.sheet.worksheet('Survivor Information')

def format_sheet[T](sheet: list[list[T]]) -> list[list[T]]:
    for r, row in enumerate(sheet):
        for c, value in enumerate(row):
            try: sheet[r][c] = int(value)
            except (ValueError, TypeError): continue
    return sheet

if ('scoring' not in st.session_state):
    st.session_state.scoring = {}

    scoring = st.session_state.sheet.worksheet('Scoring Information')
    scoring_data = format_sheet(scoring.get_all_values())

    for column in range(len(scoring_data[0])):
        column_values = [row[column] for row in scoring_data[1:]]
        for action in column_values:
            if (action != ''): st.session_state.scoring[action] = scoring_data[0][column]

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
    teams_data = format_sheet(teams.get_all_values())
    survivors_data = format_sheet(survivors.get_all_values())

    new_row = [None for _ in range(len(survivors_data[0]))]
    new_row[0] = st.session_state.title

    survivor_column = 0
    for name in st.session_state.survivor_list:
        survivor_column += 1
        survivor_points = []
        gained_points = 0
        owner = -1
        for row in range(1, len(teams_data)):
            team_survivors = teams_data[row][2].split(' | ')
            if (name in team_survivors):
                owner = row
                break

        for point in st.session_state.points:
            if (name == next(iter(point.keys()))):
                point_action = next(iter(point.values()))
                survivor_points.append(point_action)
                gained_points += st.session_state.scoring[point_action]
        
        if (survivor_points):
            new_row[survivor_column] = ' | '.join(survivor_points)

            curr_survivor_points = survivors_data[2][survivor_column]
            survivors_data[2][survivor_column] = curr_survivor_points + gained_points

            if (owner != -1):
                curr_team_points = teams_data[owner][3]
                teams_data[owner][3] = curr_team_points + gained_points

                point_breakdown = str(teams_data[owner][4])
                if (st.session_state.title in point_breakdown): point_breakdown = point_breakdown[:-9]
                else: point_breakdown += f'{st.session_state.title}:'
                for point in survivor_points: point_breakdown += f' | {name} - {point} ({st.session_state.scoring[point]})'
                point_breakdown += ' | --- | '
                teams_data[owner][4] = point_breakdown

    survivors_data.append(new_row)

    teams.update(teams_data)
    survivors.update(survivors_data)
    
    st.session_state.title = None
    st.session_state.points = []
    st.rerun()

@st.dialog('Confirm New Data')
def confirm() -> None:
    st.write('You are adding new data to the spreadsheet. It is important that this data is complete and accurate. If you are confident the data is correct, click Confirm; otherwise, click out of this dialog and verify the accuracy.')
    st.button('Confirm', on_click = confirmed)

if (st.session_state.title and st.session_state.points): st.button('Append All Points', on_click = confirm)
else: st.button('Append All Points', disabled = True)