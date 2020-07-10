import sqlite3
import config


def setup_new_group(title_group):
    connect = sqlite3.connect(database=config.name_of_db)
    cursor = connect.cursor()

    if cursor.execute('SELECT * FROM groups WHERE title_group = "{}"'.format(title_group)).fetchall():
        return 'Ошибка, данная группа уже присутствует в списке'

    result = ''

    try:
        cursor.execute('INSERT INTO groups (title_group) VALUES ("{}")'.format(title_group))
    except sqlite3.OperationalError:
        result = 'Ошибка ввода'
    else:
        result = 'Группа добавлена'
    finally:
        connect.commit()
        connect.close()
    return result
