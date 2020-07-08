import config
import requests


def parse_group(id_group):
    html_code = requests.get(f'https://api.vk.com/method/wall.get?domain={id_group}&count=2&access_token={config.vk_token}&v=5.120').text
    dict_of_code = eval(html_code.replace('false', 'False').replace('true', 'True').replace('null', 'None'))
    post = dict_of_code.get('response').get('items')[-1]
    result_dict = {}
    result_dict['text'] = post.get('text')
    attachments = post.get('attachments')
    result_dict['attachments'] = []
    for attachment in attachments:
        if attachment.get('photo'):
            result_dict.get('attachments').append(max(attachment.get('photo').get('sizes'), key=lambda x: x.get('height')).get('url').replace('\\', ''))
    return result_dict


if __name__ == '__main__':
    print(parse_group('peregovorov'))
