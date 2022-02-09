# coding: utf-8
import os
import qrcode
import json
from flask import Flask, render_template, redirect
from flask import request
from flask_cors import CORS
from make_test import make_test
from server_utils import send_line_notify, number_handling, user_list2html, test_label, book_name2_html
from mysql_db import get_bookname_from_MySQL, get_testdf_from_MySQL, register_user_list, get_userlist, get_user_id, \
    register_user_result, get_booklist, check_result_SQL, register_book_data, add_csvdata2MySQL, \
    get_bookname4_start_page
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

UPLOAD_FOLDER = './uploads'
# アップロードされる拡張子の制限
ALLOWED_EXTENSIONS = set(['csv', 'jpg'])
app = Flask(__name__)
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = "secret"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


class LoginForm(FlaskForm):
    user_name = StringField('user_name')
    password = StringField('passwprd')
    submit = SubmitField('ログイン')


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route("/")
def start_page():
    return render_template("make_test.html", booklist=user_list2html(get_booklist()),
                           bookname_list=book_name2_html(get_bookname4_start_page()))


@app.route("/t")
def make_forT():
    return render_template("make_test_forT.html", select_send2=user_list2html(get_userlist()),
                           booklist=user_list2html(get_booklist()),
                           bookname_list=book_name2_html(get_bookname4_start_page()))


@app.route("/return_test")
def return_test_page():
    start, end, how_many, is_random, which_lang, which_book, select_or_not, _ = number_handling()
    bookname_taple = get_bookname_from_MySQL(which_book)
    original_list = get_testdf_from_MySQL(bookname_taple[0])

    test_dict = make_test(original_list, start, end, how_many, which_lang, is_random, select_or_not)
    detail_str = test_label(bookname_taple[1], start, end, how_many)

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
    detail_str = test_label(bookname_taple[1], start, end, how_many)
    print(test_dict)
    return render_template("sp_quiz.html", js_code=return_json, test_detail=detail_str, user_id=user_id)


@app.route("/return_qr")
def make_qr():
    start, end, how_many, is_random, _, which_book, _, user_id = number_handling()
    detail_str = test_label(get_bookname_from_MySQL(which_book)[1], start, end, how_many)

    request_str = str(request)
    request_str = request_str.replace('<Request ', '')
    request_str = request_str.replace('[GET]>', '')
    request_str1 = request_str.replace('/return_qr', '/return_test_sp')

    QR_FILE_NAME = './static/images/qrcode.png'
    if os.path.isfile(QR_FILE_NAME):
        os.remove(QR_FILE_NAME)
    img = qrcode.make(request_str1)
    img.save(QR_FILE_NAME)

    return render_template("qr_preview.html", title=detail_str)


@app.route("/user_register", methods=["GET", "POST"])
def user_handling():
    if request.method == "GET":
        return render_template("user_register.html", error_message="")

    elif request.method == "POST":
        user_name = request.form["user_name"]

        for i in user_name:
            if i == " ":
                i = "_"

        try:

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
        user_id, which_book, test_date, correct_rate = int(request.form['send_to']), int(request.form['which_book']), \
                                                       request.form['test_date'], int(request.form[
                                                                                          'correct_rate'])
        return_table = check_result_SQL(user_id, which_book, test_date, correct_rate)

        return render_template("result_check.html", select_user=return_html, booklist=return_booklist,
                               return_table=return_table)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.user_name.data == 'Kaito' and form.password.data == 'Shinomiya':
            user = User(form.user_name.data)
            login_user(user)
            return redirect('/data_upload')
        else:
            return 'ログインに失敗しました'

    return render_template("login.html", form=form)


@app.route("/data_upload", methods=['GET', 'POST'])
@login_required
def data_upload():
    if request.method == "GET":
        return render_template("data_upload.html", result="")
    else:
        try:
            book_name_en = request.form['booklist']
            book_name_jp = request.form['bookname']
            register_book_data(book_name_en, book_name_jp)
            file = request.files['file']
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            add_csvdata2MySQL("./uploads/" + file.filename, book_name_en)
            return render_template("data_upload.html", result="登録完了")
        except:
            return render_template("data_upload.html", result="エラーが発生しました。もう一度やり直してください")


@app.route("/logout")
def logout():
    logout_user()

    return render_template("login.html")


@app.route("/register_result", methods=["POST"])
def register():
    which_book, title = request.json['which_book'], request.json['test_title']
    start, end, number_of_quiz, score = int(request.json['start']), int(request.json['end']), int(
        request.json['number_of_quiz']), int(request.json['score'])
    send_to, user_id = int(request.json['send_to']), int(request.json['user'])

    if request.json['en_or_jp'] == '0':
        en_or_jp = 'e'
    else:
        en_or_jp = 'j'

    if request.json['select_or_blank'] == '0':
        sel_or_bla = 's'
    else:
        sel_or_bla = 'b'
    correct_rate = int(score / number_of_quiz * 100)

    return_str = "「" + str(title) + "」のテストを行い正解率" + str(correct_rate) + "％でした。"

    if not user_id == 0:
        user_name = get_user_id(user_id)  # idから名前を取得する関数
    else:
        user_name = 'else'
    register_user_result(title, correct_rate, user_name, which_book, start, end, number_of_quiz, sel_or_bla, en_or_jp)

    if not send_to == 0:
        send_line_notify(return_str)

    return '完了', 200
