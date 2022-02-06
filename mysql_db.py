import mysql.connector
import datetime
import csv


def connet_MySQL(is_user=False) -> object:
    if is_user == False:
        database_name = "kaitoshinomiya_tangotest_data"
    else:
        database_name = "kaitoshinomiya_tangotest_user"
    conn = mysql.connector.connect(
        host='mysql57.kaitoshinomiya.sakura.ne.jp',
        port='3306',
        user='kaitoshinomiya',
        password='Azbi5645',
        database=database_name
    )
    cur = conn.cursor()
    return conn, cur


def close_MySQL(conn, cur, is_Commit=False):
    cur.close()
    if is_Commit:
        conn.commit()  # insertをした場合は確実にコミットしないと追加が反映されない。
    conn.close()

    return True


def get_bookname_from_MySQL(id_db):
    conn, cur = connet_MySQL()
    cur.execute("SELECT booklist,bookname FROM booklist WHERE id=%s", (id_db,))
    row = cur.fetchall()
    close_MySQL(conn, cur)
    bookname_taple = row[0]
    return bookname_taple


def get_bookname4_start_page():
    conn, cur = connet_MySQL()
    cur.execute("select booklist,bookname from booklist", )
    row = cur.fetchall()
    close_MySQL(conn, cur)

    return row


def get_booklist():
    conn, cur = connet_MySQL()
    cur.execute("SELECT id,booklist FROM booklist;")
    rows = cur.fetchall()
    close_MySQL(conn, cur)
    return rows


def get_userlist():
    conn, cur = connet_MySQL(True)
    cur.execute('SELECT * FROM user_list;')
    rows = cur.fetchall()
    close_MySQL(conn, cur)

    return rows


def get_user_id(user_id):
    conn, cur = connet_MySQL(True)
    cur.execute('SELECT name FROM user_list WHERE id=%s', (user_id,))
    row = cur.fetchall()[0][0]  # [(hogehoge,),]の形の入力
    close_MySQL(conn, cur)
    print(row)
    return row


def register_user_list(user_name):
    conn, cur = connet_MySQL(True)
    query = 'INSERT INTO user_list(name) VALUES (%s)'
    val = (user_name,)
    cur.execute(query, val)
    query = "CREATE TABLE user_" + user_name + " (`id` INT AUTO_INCREMENT primary key NOT NULL,`test_name` varchar(100) NOT NULL,`score_percent` int(10) NOT NULL,`test_date` datetime NOT NULL,`which_book`int(10) NOT NULL,`start` int(10) NOT NULL,`end` int(10) NOT NULL,`how_many` int(10) NOT NULL,`select_or_blank` varchar(100) NOT NULL,`en_or_jp` varchar(100) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    cur.execute(query)
    close_MySQL(conn, cur, True)

    return True


def register_book_data(book_name_en, book_name_jp):
    conn, cur = connet_MySQL()
    query = 'INSERT INTO booklist(booklist,bookname) VALUES (%S,%S)'
    val = (book_name_en, book_name_jp)
    cur.execute(query, val)
    query = "CREATE TABLE " + book_name_en + " (`id` INT AUTO_INCREMENT primary key NOT NULL,`english` varchar(100),`japanese` varchar(100)) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    cur.execute(query)
    close_MySQL(conn, cur, True)
    return True


def register_user_result(test_title, score_rate, user_name, which_book, start, end, how_many, sel_or_bla, en_or_jp):
    now = datetime.datetime.now()
    conn, cur = connet_MySQL(True)
    query = 'INSERT INTO user_' + user_name + '(test_name,score_percent,test_date,which_book,start,end,how_many,select_or_blank,en_or_jp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    values = (
        test_title, score_rate, now.strftime('%Y-%m-%d %H:%M:%S'), which_book, start, end, how_many, sel_or_bla,
        en_or_jp)
    cur.execute(query, values)
    close_MySQL(conn, cur, True)

    return True


def get_testdf_from_MySQL(db_name):
    conn, cur = connet_MySQL()
    query = 'SELECT english,japanese FROM ' + db_name
    cur.execute(query)
    rows = cur.fetchall()
    close_MySQL(conn, cur)

    return rows


def check_result_SQL(user_id, which_book, test_date, correct_rate):
    conn, cur = connet_MySQL(True)
    if not user_id == 0:
        cur.execute('SELECT name FROM user_list WHERE id=%s', (user_id,))
        user_name = 'user_' + cur.fetchall()[0][0]
    else:
        user_name = 'user_else'

    if not which_book == 0:
        refer_book_str = ' and which_book = ' + str(which_book)
    else:
        refer_book_str = ''

    query = 'SELECT test_name,which_book,score_percent,test_date from ' + user_name + ' where score_percent <= ' + str(
        correct_rate) + refer_book_str + ' and test_date >= (NOW() - INTERVAL ' + str(
        test_date) + ' DAY) ORDER BY id DESC'
    cur.execute(query)
    rows = cur.fetchall()
    close_MySQL(conn, cur)

    return_list = []
    for row in rows:
        row_list = []
        for i in range(len(row)):
            if i == 1:
                row_list.append(get_bookname_from_MySQL(row[i])[1])
            else:
                row_list.append(row[i])
        return_list.append(row_list)

    return return_list


def add_csvdata2MySQL(file_path, filename_en):
    conn, cur = connet_MySQL()
    with open(file_path) as f:
        reader = csv.reader(f)
        i = 1
        for row in reader:
            a = str(row[1])
            b = str(row[2])

            cur.execute("INSERT INTO " + filename_en + " VALUES (%s, %s, %s)", (i, a, b))
            i = i + 1
    close_MySQL(conn, cur, True)

    return True


def post_test_result(user_id):
    conn, cur = connet_MySQL()

    if user_id == 0:
        cur.execute()  # 単純にテストの結果を通知する。

    return True
