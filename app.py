import streamlit as st

import pandas as pd
import plotly.express as px

from db_func import (create_table, add_data, view_all_data,
                     view_uniqe_task, get_task, edit_task_data,
                     delete_data, create_usertable, add_userdata,
                     login_user)


def main():
    """Simple login App"""

    st.title('Login App')
    menu = ['Home', 'Login', 'SignUp']

    choice_1 = st.sidebar.selectbox('Menu', menu)

    if choice_1 == 'Home':
        st.subheader('Home')

    elif choice_1 == 'Login':
        st.subheader('Login Section')

        username = st.sidebar.text_input('User Name')
        password = st.sidebar.text_input('Password', type='password')

        menu = ['Create', 'Read', 'Update', 'Delete', 'About']
        choice = st.selectbox('Menu', menu)

        if st.sidebar.checkbox('Login'):
            create_usertable()
            result = login_user(username, password)
            if result:
                st.success('Logged In as {}'.format(username))
                create_table(username, password)
                if choice == 'Create':
                    st.subheader('Add Orders')

                    # Layout
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        # task = st.text_area('Task To Do')
                        task_code = st.text_input('Enter Code')
                    with col2:
                        # task_status = st.selectbox('Status', ['To Do', 'Doing', 'Done'])
                        # task_due_date = st.date_input('Due date')
                        task_name = st.text_area('Enter Name')
                    with col3:
                        task_unit = st.text_input('Enter Unit')
                    with col4:
                        task_qty = st.text_input('Enter Qty')

                    if st.button('Add Order'):
                        add_data(username, password, task_code, task_name, task_unit, task_qty)
                        st.success('Successfully Added Order: {}'.format(task_code))
                elif choice == 'Read':
                    st.subheader('View Items')
                    result = view_all_data(username, password)
                    # st.write(result)
                    df = pd.DataFrame(result, columns=['Code', 'Name', 'Unit', 'Qty'])
                    with st.expander('**View All Data**'):
                        # df = pd.DataFrame(result, columns=['Task','Status', 'Task due date'])
                        st.dataframe(df)

                    with st.expander('**Task Status**'):
                        task_df = df['Code'].value_counts().to_frame()
                        # st.dataframe(task_df)
                        task_df = task_df.reset_index()
                        st.dataframe(task_df)

                        p1 = px.pie(task_df, names='index', values='Code')
                        st.plotly_chart(p1)
                elif choice == 'Update':
                    st.subheader('Edit/Update Items')
                    result = view_all_data(username, password)
                    # st.write(result)
                    df = pd.DataFrame(result, columns=['Code', 'Name', 'Unit', 'Qty'])
                    with st.expander('**Current All Data**'):
                        # df = pd.DataFrame(result, columns=['Task','Status', 'Task due date'])
                        st.dataframe(df)

                        # st.write(view_uniqe_task())
                        list_of_task = [i[0] for i in view_uniqe_task(username, password)]
                        # st.write(list_of_task)

                        selected_task = st.selectbox('Order To Edit', list_of_task)

                        selected_result = get_task(username, password, selected_task)
                        # st.write(selected_result)

                        if selected_result:
                            task_code = selected_result[0][0]
                            task_name = selected_result[0][1]
                            task_unit = selected_result[0][2]
                            task_qty = selected_result[0][3]
                            # Layout
                            col1, col2, col3, col4 = st.columns(4)

                            with col1:
                                new_task_code = st.text_input('Task To Do', task_code)

                            with col2:
                                new_task_name = st.text_area(task_name)
                            with col3:
                                new_task_unit = st.text_input(task_unit)
                            with col4:
                                new_task_qty = st.text_input(task_qty)

                            if st.button('Update Task'):
                                edit_task_data(username, password, new_task_code, new_task_name, new_task_unit,
                                               new_task_qty,
                                               task_code, task_name, task_unit, task_qty)
                                # add_data(new_task, new_task_status, new_task_due_date)
                                st.success('Successfully Updated:: {} To ::{}'.format(task_code, new_task_code))

                    result2 = view_all_data(username, password)
                    df = pd.DataFrame(result2, columns=['Code', 'Name', 'Unit', 'Qty'])
                    with st.expander('**Updated All Data**'):
                        st.dataframe(df)

                elif choice == 'Delete':
                    st.subheader('Delete Items')
                    result = view_all_data(username, password)
                    df = pd.DataFrame(result, columns=['Code', 'Name', 'Unit', 'Qty'])
                    with st.expander('**Current All Data**'):
                        st.dataframe(df)

                    # st.write(view_uniqe_task())
                    list_of_task = [i[0] for i in view_uniqe_task(username, password)]
                    # st.write(list_of_task)
                    selected_task = st.selectbox('Task To Delete', list_of_task)
                    st.warning('**DO YOU WANT TO DELETE: ({})?**'.format(selected_task))
                    if st.button('Delete Data'):
                        delete_data(username, password, selected_task)
                        st.success('**Data has been successfully deleted**')

                    new_result = view_all_data(username, password)
                    df2 = pd.DataFrame(new_result, columns=['Code', 'Name', 'Unit', 'Qty'])
                    with st.expander('**Updated All Data**'):
                        st.dataframe(df2)

                else:
                    st.subheader('About')
            else:
                st.warning('Incorrect Username/Password')
                st.info('OR Signup For A New Account')
    elif choice_1 == 'SignUp':
        st.subheader('Create New Account')
        new_user = st.text_input('Username')
        new_password = st.text_input('Password', type='password')

        if st.button('Signup'):
            create_usertable()
            add_userdata(new_user, new_password)
            st.success('You have successfully created a valid Account')
            st.info('Go to Login Menu to login')

    # new_task_due_date ---- HIDE STREAMLIT STYLE ----
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
