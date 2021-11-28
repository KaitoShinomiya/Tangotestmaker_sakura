import mysql.connector
import datetime


def connet_MySQL(is_user = False) -> object:
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

def get_booklist():
    conn, cur = connet_MySQL()
    cur.execute("SELECT id,booklist FROM booklist;")
    rows = cur.fetchall()
    close_MySQL(conn,cur)
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
    query = "CREATE TABLE user_" + user_name + " (`id` INT AUTO_INCREMENT primary key NOT NULL,`test_name` varchar(100) NOT NULL,`score_percent` int(10) NOT NULL,`test_date` datetime NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    cur.execute(query)
    close_MySQL(conn, cur, True)

    return True


def register_user_result(test_title, score_rate, user_name):
    now = datetime.datetime.now()
    conn, cur = connet_MySQL(True)
    query = 'INSERT INTO user_' + user_name + '(test_name,score_percent,test_date) VALUES(%s,%s,%s)'
    values = (test_title, score_rate, now.strftime('%Y-%m-%d %H:%M:%S'))
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




def post_test_result(user_id):
    conn, cur = connet_MySQL()

    if user_id == 0:
        cur.execute()  # 単純にテストの結果を通知する。

    return True
