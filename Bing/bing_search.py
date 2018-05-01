# coding:utf-8
import contextlib
import pymysql
from MagicBing import MagicBing
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

PROXIES = [
    {'https': 'https://218.60.8.98:3129', }
]

mg = MagicBing(PROXIES)

# 定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql(host='127.0.0.1', port=3306, user='root', passwd='P@ssw0rd', db='amazon_db', charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def insert_mysql(offer_dict_list, table_name):
    insert_into_sql = "INSERT INTO " + table_name + "("
    insert_into_sql_s = ""
    datas = []
    try:
        if offer_dict_list and offer_dict_list[0]:
            keys = offer_dict_list[0].keys()
            for j in keys:
                insert_into_sql = insert_into_sql + j + ","
                insert_into_sql_s = insert_into_sql_s + "%s,"
            insert_into_sql = insert_into_sql.rstrip(",") + ") VALUES (" + insert_into_sql_s.rstrip(',') + ")"
            print insert_into_sql
        else:
            return
    except Exception as e:
        print("Splicing insert_into_" + table_name + "_sql errors:{}".format(e))

    try:
        for i in offer_dict_list:
            data = tuple(i.values())
            datas.append(data)
    except Exception as e:
        print("Splicing insert_into_" + table_name + "_data errors:{}".format(e))

    try:
        with mysql() as cursor:
            cursor.executemany(insert_into_sql, datas)
    except Exception as e:
        print("INSERT " + table_name + " errors:{}".format(e), datas)


def bing_search():
    postfix = open('../config/postfix', 'r')
    postfix = postfix.readline()

    with mysql() as cursor:
        try:
            row_count = cursor.execute("SELECT DISTINCT key_state, key_word from key_word where key_state is null limit 1000")
            print "---------------------------ALL KEYWORD:"+str(row_count)+"---------------------------"
            keywords = []
            for row in cursor.fetchall():
                keyword = row["key_word"]
                if row["key_state"]:
                    row["key_state"] = row["key_state"]+"US;"
                else:
                    row["key_state"] = "US;"
                keywords.append(row)
                result_keyword = []
                for p in range(0, 80):
                    first = p * 10 + 1
                    result_keyword_one = mg.search(query=keyword + postfix, first=first, keyword=keyword)
                    result_keyword = result_keyword + result_keyword_one

                insert_mysql(result_keyword, "listing_google")
            update_key_word(keywords)
        except Exception as e:
            print("---------------------------KEYWORD ERROR:"+str(row_count)+"---------------------------{}".format(e))
            update_key_word(keywords)


def update_key_word(keywords):
    update_sql = "UPDATE key_word set key_state = %s  where key_word = %s"
    datas = []
    try:
        for i in keywords:
            data = (i["key_state"], i["key_word"])
            datas.append(data)
    except Exception as e:
        print("Splicing UPDATE key_word data errors:{}".format(e))
    try:
        with mysql() as cursor:
            row_count = cursor.executemany(update_sql, datas)
            print("UPDATE listing_google {}/{} success:", row_count, len(keywords))
    except Exception as e:
        print("UPDATE listing_google errors:{}".format(e), keywords)


bing_search()
