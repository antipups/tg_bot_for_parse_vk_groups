import config
import requests
import sqlite3


def parse_group():
    """
        Парсим вк группы, берем их из БД, и после парсим
    :return:
    """

    connect = sqlite3.connect(database=config.name_of_db)
    cursor = connect.cursor()

    groups = (row[0] for row in cursor.execute('SELECT title_group FROM groups'))
    for group in tuple(groups):
        html_code = requests.get(
            f'https://api.vk.com/method/wall.get?domain={group}&count=2&access_token={config.vk_token}&v=5.120').text
        dict_of_code = eval(html_code.replace('false', 'False').replace('true', 'True').replace('null', 'None'))
        post = dict_of_code.get('response').get('items')[-1]
        if cursor.execute('SELECT * '  # если такая запись уже публикаовалось - бан
                          'FROM posts '
                          f'WHERE posts.id_group = "{group}" '
                          f'    AND posts.id_post = {post.get("id")}').fetchall():
            continue
        # else:
        #     cursor.execute(f'INSERT INTO posts (id_group, id_post) VALUES ("{group}", {post.get("id")})')
        #     connect.commit()

        result_dict = {'id': post.get('id'), 'text': post.get('text')}
        attachments = post.get('attachments')
        result_dict['attachments'] = []
        if attachments:
            for attachment in attachments:
                if attachment.get('photo'):
                    result_dict.get('attachments').append(requests.get(
                        max(attachment.get('photo').get('sizes'), key=lambda x: x.get('height')).get('url').replace('\\',
                                                                                                                    '')).content)
        if not post.get('text') and not post.get('attachments'):
            continue
        yield result_dict
    connect.close()


if __name__ == '__main__':
    print(parse_group())


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
