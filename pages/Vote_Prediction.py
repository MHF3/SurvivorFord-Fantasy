import streamlit as st

st.sidebar.page_link('Log_In.py')
st.sidebar.page_link('pages/Team_Information.py')
st.sidebar.page_link('pages/League_Standings.py')
if (st.user.email in st.secrets['admin_emails']):
    st.sidebar.page_link('pages/Update_Spreadsheet.py')
    st.sidebar.page_link('pages/Toggle_Lock.py')

teams = st.session_state.sheet.worksheet('Team Information')

if ('team_row' not in st.session_state):
    try: st.session_state.team_row = teams.col_values(1).index(st.user.email) + 1
    except ValueError: st.session_state.team_row = -1

if (st.session_state.team_row == -1): st.header('Sign up through the link in the GroupMe to create your team!')
else:
    GROUP_POINTS = 10

    if ('locked' not in st.session_state): st.session_state.locked = bool(st.session_state.sheet.worksheet('Locked').cell(1, 1).numeric_value)

    if (st.session_state.locked): st.header('Vote Predictions Locked')
    else: st.header('Make Your Vote Predictions')

    if ('predicted_survivors' not in st.session_state): st.session_state.predicted_survivors = []
    if ('groups' not in st.session_state):
        survivors_data = st.session_state.sheet.worksheet('Survivor Information').get_all_values()
        groups = {}
        for i in range(1, len(survivors_data[0])):
            if (survivors_data[1][i] != 'Out' and survivors_data[1][i] != 'Jury'):
                if (survivors_data[1][i] in groups.keys()):
                    members = groups[survivors_data[1][i]]
                    members.append(survivors_data[0][i])
                    groups[survivors_data[1][i]] = members
                else: groups[survivors_data[1][i]] = [survivors_data[0][i]]
        st.session_state.groups = groups

    def allocate_point(group: str, survivor: str) -> None:
        st.session_state[group] -= 1
        if (survivor not in st.session_state):
            st.session_state[survivor] = 1
            st.session_state.predicted_survivors.append(survivor)
        else: st.session_state[survivor] += 1

    def unallocate_point(group: str, survivor: str) -> None:
        st.session_state[group] += 1
        st.session_state[survivor] -= 1
        if (st.session_state[survivor] == 0):
            del st.session_state[survivor]
            st.session_state.predicted_survivors.remove(survivor)

    if ('checked_predictions' not in st.session_state):
        curr_predictions = teams.cell(st.session_state.team_row, 6).value
        if (curr_predictions):
            curr_predictions_list = curr_predictions.split(' | ')
            curr_predicted_dict = dict(curr_prediction.split(' - ') for curr_prediction in curr_predictions_list)
            for group in st.session_state.groups.keys():
                if (group not in st.session_state): st.session_state[group] = GROUP_POINTS
                for survivor in st.session_state.groups[group]:
                    if (survivor in curr_predicted_dict.keys()):
                        for _ in range(int(curr_predicted_dict[survivor])): allocate_point(group, survivor)
        st.session_state.checked_predictions = True

    for group in st.session_state.groups.keys():
        with st.container(border = True):
            if (group not in st.session_state): st.session_state[group] = GROUP_POINTS
            st.subheader(f'{group} - {st.session_state[group]} Points to Allocate')
            for survivor in st.session_state.groups[group]:
                column_name, column_minus, column_count, column_add = st.columns([0.75, 0.1, 0.05, 0.1], gap = None, vertical_alignment = 'center')
                with column_name: st.write(survivor)
                if (survivor in st.session_state):
                    with column_minus:
                        if (st.session_state.locked): st.button('', f'{survivor}_unallocate', icon = ':material/remove:', disabled = True)
                        else: st.button('', f'{survivor}_unallocate', on_click = unallocate_point, args = (group, survivor), icon = ':material/remove:')
                    with column_count: st.write(f'**{st.session_state[survivor]}**')
                else:
                    with column_minus: st.button('', f'{survivor}_unallocate', icon = ':material/remove:', disabled = True)
                    with column_count: st.write(f'**0**')
                if (st.session_state[group]):
                    with column_add:
                        if (st.session_state.locked): st.button('', f'{survivor}_allocate', icon = ':material/add_2:', disabled = True)
                        else: st.button('', f'{survivor}_allocate', on_click = allocate_point, args = (group, survivor), icon = ':material/add_2:')
                else:
                    with column_add: st.button('', f'{survivor}_allocate', icon = ':material/add_2:', disabled = True)

    if (st.session_state.locked): st.button('Update Predictions', icon = ':material/upload:', disabled = True)
    else:
        if (st.button('Update Predictions', icon = ':material/upload:')):
            vote_predictions = ''
            for survivor in st.session_state.predicted_survivors: vote_predictions += f'{survivor} - {st.session_state[survivor]} | '
            vote_predictions = vote_predictions[:-3]
            teams.update_cell(st.session_state.team_row, 6, vote_predictions)