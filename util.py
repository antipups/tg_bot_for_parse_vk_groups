import sqlite3
import config


def setup_new_group(title_group):
    connect = sqlite3.connect(database=config.name_of_db)
    cursor = connect.cursor()

    if cursor.execute(f'SELECT * FROM groups WHERE title_group = "{title_group}"').fetchall():
        return 'Ошибка, данная группа уже присутствует в списке'

    result = ''

    try:
        cursor.execute(f'INSERT INTO groups (title_group) VALUES ("{title_group}")')
    except sqlite3.OperationalError:
        result = 'Ошибка ввода'
    else:
        result = 'Группа добавлена'
    finally:
        connect.commit()
        connect.close()
    return result


# def setup_new_channel(name_channel, id_):
#     connect = sqlite3.connect(database=config.name_of_db)
#     cursor = connect.cursor()
#
#     if cursor.execute(f'SELECT * FROM channels WHERE id = {id_}').fetchall():
#         return
#
#     cursor.execute(f'INSERT INTO channels (id_channel, title_channel) VALUES ({id_}, {name_channel})')
#     connect.commit()
#     connect.close()
#
#
# def get_channels():
#     connect = sqlite3.connect(database=config.name_of_db)
#     cursor = connect.cursor()
#
#     result = cursor.execute('SELECT * FROM channels').fetchall()
#
#     connect.close()
#     return result
