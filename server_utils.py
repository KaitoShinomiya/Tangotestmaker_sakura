import requests
import os
from flask import request


def number_handling():
    is_random = int(request.args.get('sequence_or_random'))
    start, end, = int(request.args.get("start")), int(request.args.get("end"))
    which_lang = int(request.args.get("which_lang"))
    which_book = int(request.args.get('which_book'))
    select_or_not = int(request.args.get('select_or_not'))
    if 'user' in request.args:
        user_id = int(request.args.get('user'))
    else:
        user_id = 0
    if is_random == 1:
        how_many = int(request.args.get("how_many"))
    else:
        how_many = end + 1 - start

    return start, end, how_many, is_random, which_lang, which_book, select_or_not, user_id


def user_list2html(list_of_user):
    return_html = ""
    if not list_of_user == 0:
        for user in list_of_user:
            value, name = str(user[0]), str(user[1])
            user_html = "<option value=" + value + ">" + name + "</option>"
            return_html = return_html + user_html
    else:
        return_html = ""
    return return_html


def send_line_notify(message):
    try:

        line_notify_token = os.environ["line_notify_token"]
        line_notify_api = os.environ['line_notify_api']
        headers = {'Authorization': f'Bearer {line_notify_token}'}
        data = {'message': str(message)}
        res = requests.post(line_notify_api, headers=headers, data=data)
        return True
    except Exception as e:
        return False


def test_label(which_book, start, end, how_many):
    detail_str = which_book + "  " + str(start) + "番から" + str(end) + "番: " + str(how_many) + "問"

    return detail_str


def book_name2_html(rows):
    return_str = ""
    for row in rows:
        return_str = return_str + str(row[0]) + " : " + str(row[1]) + "<br>"

    return return_str

class Counter:
    counter = 0

    def __init__(self):
        self.counter = 0

    def add(self):
        self.counter += 1
