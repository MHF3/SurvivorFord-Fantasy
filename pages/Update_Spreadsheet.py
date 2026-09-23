import streamlit as st

st.sidebar.page_link('Log_In.py')
st.sidebar.page_link('pages/Team_Information.py')
st.sidebar.page_link('pages/Vote_Prediction.py')
st.sidebar.page_link('pages/League_Standings.py')
if (st.user.email in st.secrets['admin_emails']): st.sidebar.page_link('pages/Toggle_Lock.py')

survivors = st.session_state.sheet.worksheet('Survivor Information')
scoring = st.session_state.sheet.worksheet('Scoring Information')

def format_sheet[T](sheet: list[list[T]]) -> list[list[T]]:
    for r, row in enumerate(sheet):
        for c, value in enumerate(row):
            try: sheet[r][c] = int(value)
            except (ValueError, TypeError): continue
    return sheet

if ('scoring' not in st.session_state):
    st.session_state.scoring = {}

    scoring_data = format_sheet(scoring.get_all_values())

    for column in range(len(scoring_data[0])):
        column_values = [row[column] for row in scoring_data[1:]]
        for action in column_values:
            if (action != ''): st.session_state.scoring[action] = scoring_data[0][column]

st.header('Add New Episode Scores')

if ('points' not in st.session_state): st.session_state.points = []
if ('survivor_list' not in st.session_state): st.session_state.survivor_list = [survivor for survivor in survivors.row_values(1)[1:]]
if ('playing_survivor_list' not in st.session_state):
    survivor_name_status = survivors.get_all_values()[:2]
    st.session_state.playing_survivor_list = [survivor_name_status[0][survivor] for survivor in range(1, len(survivor_name_status[0])) if (survivor_name_status[1][survivor] != 'Out' and survivor_name_status[1][survivor] != 'Jury')]
if ('action_list' not in st.session_state):
    st.session_state.action_list = [action for column in range(scoring.column_count) for action in scoring.col_values(column + 1)[1:]]
    st.session_state.action_list.remove('Voted Out (Pre-Jury)')
    st.session_state.action_list.remove('Voted Out (On Jury)')

st.text_input('Row Title', key = 'title', placeholder = 'Ex. Episode 1', persist_state = 'session')

def add_points() -> None:
    st.session_state.points.append({st.session_state.survivor: st.session_state.action})
    st.session_state.survivor = None
    st.session_state.action = None

def undo_point() -> None: st.session_state.points.pop()

with st.container(border = True):
    column_name, column_action = st.columns(2)

    with column_name:
        st.selectbox('Survivor', st.session_state.playing_survivor_list, None, key = 'survivor', placeholder = 'Who scored points', persist_state = 'session')
        if (st.session_state.survivor and st.session_state.action): st.button('Add Points', on_click = add_points)
        else: st.button('Add Points', disabled = True)
    with column_action:
        st.selectbox('Action', st.session_state.action_list, None, key = 'action', placeholder = 'What scored points', persist_state = 'session')
        if (st.session_state.points): st.button('Undo Last Point', on_click = undo_point)
        else: st.button('Undo Point', disabled = True)

    with st.expander('Current Added Points'):
        for point in st.session_state.points: st.caption(f'{next(iter(point.keys()))}: {next(iter(point.values()))}')

column_voted, column_jury = st.columns(2, vertical_alignment = 'bottom')

with column_voted: st.selectbox('Voted', st.session_state.playing_survivor_list, None, key = 'voted', placeholder = 'Who was voted out', persist_state = 'session')
with column_jury: st.toggle('On Jury', key = 'jury', persist_state = 'session')

def confirmed() -> None:
    teams = st.session_state.sheet.worksheet('Team Information')
    teams_data = format_sheet(teams.get_all_values())
    survivors_data = format_sheet(survivors.get_all_values())

    if ('Jury' in survivors_data[1]): jury_exists = True
    else: jury_exists = False

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

        survivor_index = survivors_data[0].index(name)
        if (jury_exists):
            if (survivors_data[1][survivor_index] == 'Jury'):
                survivor_points.append('Voted Out (On Jury)')
                gained_points += 1
        else:
            if (survivors_data[1][survivor_index] == 'Out'):
                survivor_points.append('Voted Out (Pre-Jury)')
                gained_points += 1

        if (survivor_points):
            new_row[survivor_column] = ' | '.join(survivor_points)

            curr_survivor_points = survivors_data[2][survivor_column]
            survivors_data[2][survivor_column] = curr_survivor_points + gained_points

            if (owner != -1):
                curr_team_points = teams_data[owner][3]
                teams_data[owner][3] = curr_team_points + gained_points

                point_breakdown = teams_data[owner][4]
                if (st.session_state.title in point_breakdown): point_breakdown = point_breakdown[:-9]
                else: point_breakdown += f'{st.session_state.title}:'
                for point in survivor_points: point_breakdown += f' | {name} - {point} ({st.session_state.scoring[point]})'
                point_breakdown += ' | --- | '
                teams_data[owner][4] = point_breakdown

    for owner in range(1, len(teams_data)):
        if (teams_data[owner][5]):
            predicted_list = teams_data[owner][5].split(' | ')
            predicted_dict = dict(prediction.split(' - ') for prediction in predicted_list)
            if (st.session_state.voted in predicted_dict):
                curr_team_points = teams_data[owner][3]
                teams_data[owner][3] = curr_team_points + int(predicted_dict[st.session_state.voted])
                point_breakdown = teams_data[owner][4][:-6]
                point_breakdown += f'Predicted {st.session_state.voted} Vote ({predicted_dict[st.session_state.voted]}) | --- | '
                teams_data[owner][4] = point_breakdown
            teams_data[owner][5] = ''

    survivors_data.append(new_row)

    voted_survivor = survivors_data[0].index(st.session_state.voted)
    if (st.session_state.jury): survivors_data[1][voted_survivor] = 'Jury'
    else: survivors_data[1][voted_survivor] = 'Out'

    teams.update(teams_data)
    survivors.update(survivors_data)

    if ('team_points' in st.session_state): del st.session_state['team_points']
    if ('team_breakdown' in st.session_state): del st.session_state['team_breakdown']
    if ('team_scores' in st.session_state): del st.session_state['team_scores']
    if ('predicted_survivors' in st.session_state): del st.session_state['predicted_survivors']
    if ('groups' in st.session_state):
        groups_delete = [group for group in st.session_state.groups.keys()]
        for group in groups_delete:
            for survivor in st.session_state.groups[group]:
                if (survivor in st.session_state): del st.session_state[survivor]
            del st.session_state[group]
        del st.session_state['groups']

    st.session_state.title = None
    st.session_state.voted = None
    st.session_state.points = []
    st.session_state.jury = False
    st.rerun()

@st.dialog('Confirm New Data')
def confirm() -> None:
    st.write('You are adding new data to the spreadsheet. It is important that this data is complete and accurate. If you are confident the data is correct, click Confirm; otherwise, click out of this dialog and verify the accuracy.')
    st.button('Confirm', on_click = confirmed)

# if (st.session_state.title and st.session_state.points and st.session_state.voted): st.button('Update', on_click = confirm)
if (st.session_state.title and st.session_state.voted): st.button('Update', on_click = confirm, icon = ':material/database_upload:')
else: st.button('Update', icon = ':material/database_upload:', disabled = True)