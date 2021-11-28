# coding: utf-8
import os
import qrcode
import json
from flask import Flask, render_template, send_from_directory, redirect, Markup
from flask import request
from flask_cors import CORS
from make_test import make_test
from server_utils import send_line_notify, number_handling, user_list2html
from mysql_db import get_bookname_from_MySQL, get_testdf_from_MySQL, register_user_list, get_userlist, get_user_id, \
    register_user_result, get_booklist

app = Flask(__name__)
CORS(app)


@app.route("/check")
def index():
    return "Hello Flask!"


@app.route("/")
def start_page():
    return_booklist = user_list2html(get_booklist())
    return render_template("make_test.html", booklist=return_booklist)


@app.route("/t")
def make_forT():
    return_html = user_list2html(get_userlist())
    return_booklist = user_list2html(get_booklist())

    return render_template("make_test_forT.html", select_send2=return_html, booklist=return_booklist)


@app.route("/return_test")
def return_test_page():
    start, end, how_many, is_random, which_lang, which_book, select_or_not, _ = number_handling()
    bookname_taple = get_bookname_from_MySQL(which_book)
    original_list = get_testdf_from_MySQL(bookname_taple[0])

    test_dict = make_test(original_list, start, end, how_many, which_lang, is_random, select_or_not)
    detail_str = bookname_taple[1] + "  " + str(start) + "番から" + str(end) + "番: " + str(how_many) + "問"

    if select_or_not == 0:
        return render_template("tangotest_select.html", detail=detail_str, return_table=test_dict)
    else:
        return render_template("tangotest_not.html", detail=detail_str, return_table=test_dict)


@app.route("/return_test_sp")
def sp_return_page():
    start, end, how_many, is_random, which_lang, which_book, _, user_id = number_handling()
    select_or_not = 0
    bookname_taple = get_bookname_from_MySQL(which_book)
    original_df = get_testdf_from_MySQL(bookname_taple[0])

    test_dict = make_test(original_df, start, end, how_many, which_lang, is_random, select_or_not)
    return_json = json.dumps(test_dict, ensure_ascii=False)
    detail_str = bookname_taple[1] + "  " + str(start) + "番から" + str(end) + "番: " + str(how_many) + "問"
    return render_template("sp_quiz.html", js_code=return_json, test_detail=detail_str, user_id=user_id)


@app.route("/return_qr")
def make_qr():
    start, end, how_many, is_random, _, which_book, _, user_id = number_handling()
    bookname_taple = get_bookname_from_MySQL(which_book)
    detail_str = bookname_taple[1] + "  " + str(start) + "番から" + str(end) + "番: " + str(how_many) + "問"

    request_str = str(request)
    request_str = request_str.replace('<Request ', '')
    request_str = request_str.replace('[GET]>', '')
    request_str1 = request_str.replace('/return_qr', '/return_test_sp')

    QR_FILE_NAME = './static/images/qrcode.png'
    if os.path.isfile(QR_FILE_NAME):
        os.remove(QR_FILE_NAME)
    img = qrcode.make(request_str1)
    img.save(QR_FILE_NAME)

    return render_template("qr_preview.html", h5_ttitle=detail_str)


@app.route("/user_register", methods=["GET", "POST"])
def user_handling():
    if request.method == "GET":
        return render_template("user_register.html", error_message="")

    elif request.method == "POST":
        user_name = request.form["user_name"]
        try:
            # SQLへのデータ登録
            register_user_list(user_name)
            return render_template("user_register.html", error_message="登録完了しました！")

        except Exception as e:
            return render_template("user_register.html", error_message="既に登録されている名前です。別の名前で登録してください。")


@app.route("/result_check", methods=["GET", "POST"])
def result_check():
    return_html = user_list2html(get_userlist())
    return_booklist = user_list2html(get_booklist())
    if request.method == "GET":

        return render_template("result_check.html", select_user=return_html, booklist=return_booklist)
    elif request.method == "POST":
        # 期間指定、本の指定、正解率の指定で絞りができるとなお良いと思う。
        return render_template("result_check.html", select_user=return_html, booklist=return_booklist)


@app.route("/register_result", methods=["POST"])
def register():
    title = request.json['test_title']
    score = int(request.json['score'])
    number_of_quiz = int(request.json['number_of_quiz'])
    send_to = int(request.json['send_to'])
    user_id = int(request.json['user'])
    correct_rate = int(score / number_of_quiz * 100)
    return_str = "「" + str(title) + "」のテストを行い正解率" + str(correct_rate) + "％でした。"

    if not user_id == 0:
        user_name = get_user_id(user_id)  # idから名前を取得する関数
    else:
        user_name = 'else'
    register_user_result(title, correct_rate, user_name)

    if not send_to == 0:
        send_line_notify(return_str)

    return '完了', 200