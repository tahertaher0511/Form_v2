import sqlite3

conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()


def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')


def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username, password) VALUES (?, ?)', (username, password))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password =?', (username, password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM usertable')
    data = c.fetchall()
    return data


def create_table(username, password):
    c.execute('CREATE TABLE IF NOT EXISTS {}{}(code TEXT, name TEXT, unit TEXT, qty TEXT)'.format(username, password))


def add_data(username, password, code, name, unit, qty):
    c.execute(f'INSERT INTO {username}{password}(code, name, unit, qty) VALUES (?, ?, ?, ?)', (code, name, unit, qty))
    conn.commit()


def view_all_data(username, password):
    c.execute('SELECT * FROM {}{}'.format(username, password))
    data = c.fetchall()
    return data


def view_uniqe_task(username, password):
    c.execute(f'Select DISTINCT code from {username}{password}')
    data = c.fetchall()
    return data


def get_task(username, password, code):
    c.execute('SELECT * FROM {}{} WHERE code="{}"'.format(username, password, code))
    # c.execute('SELECT * FROM tasktable WHERE task=?', (task))
    data = c.fetchall()
    return data


def edit_task_data(username, password, new_task_code, new_task_name, new_task_unit, new_task_qty, task_code, task_name,
                   task_unit, task_qty):
    c.execute(
        'UPDATE "{}{}" SET code ="{}", name="{}", unit="{}", qty="{}" WHERE code ="{}" AND '
        'name="{}" AND unit="{}" AND qty'.format(
            username, password, new_task_code, new_task_name, new_task_unit, new_task_qty, task_code, task_name,
            task_unit, task_qty))
    conn.commit()
    data = c.fetchall()
    return data


def delete_data(username, password, code):
    c.execute('DELETE FROM {}{} WHERE code="{}"'.format(username, password, code))
    conn.commit()
