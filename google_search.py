# coding:utf-8
import contextlib
import os
import sys
import random
import time
import logging
import pymysql
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from MagicGoogle import MagicGoogle

################################################
# """
# cd MagicGoogle
# python Examples/search_result.py
# """
#################################################

PROXIES = [{
    'http': 'http://152.204.130.86:3128',
    'https': 'https://152.204.130.86:3128',
}]

# Or MagicGoogle()
mg = MagicGoogle()

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("chardet").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')
LOGGER = logging.getLogger('google_search.py')


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
        else:
            return
    except Exception as e:
        LOGGER.info("Splicing insert_into_" + table_name + "_sql errors:{}".format(e))

    try:
        for i in offer_dict_list:
            data = tuple(i.values())
            datas.append(data)
    except Exception as e:
        LOGGER.info("Splicing insert_into_" + table_name + "_data errors:{}".format(e))

    try:
        with mysql() as cursor:
            cursor.executemany(insert_into_sql, datas)
    except Exception as e:
        LOGGER.info(insert_into_sql)
        LOGGER.info("INSERT " + table_name + " errors:{}".format(e), datas)


def google_search():
    postfix = open('./config/postfix', 'r')
    postfix = postfix.readline()

    with mysql() as cursor:
        try:
            row_count = cursor.execute(
                "SELECT  key_state, key_word from key_word_us where key_state is null  ORDER BY key_utime desc ")
            LOGGER.info("----------------ALL KEYWORD:" + str(row_count) + "-----------------")
            for row in cursor.fetchall():
                keywordone = []
                keyword = row["key_word"]

                if row["key_state"]:
                    row["key_state"] = row["key_state"] + "US;"
                else:
                    row["key_state"] = "US;"
                num = 400
                results_per_page = 100
                if num % results_per_page == 0:
                    pages = num / results_per_page
                else:
                    pages = num / results_per_page + 1
                result_keyword = []
                for p in range(0, pages):
                    start = p * results_per_page
                    get_url_sleep_time = random.randint(2, 5)
                    result_keyword_one, result_num = mg.search(query=keyword + postfix, num=results_per_page,
                                                               language='en', start=start,
                                                               pause=get_url_sleep_time, keyword=keyword,)
                    result_keyword = result_keyword + result_keyword_one
                    insert_mysql(result_keyword_one, "listing_google_us")
                    time.sleep(get_url_sleep_time)
                    if result_num < start + 100:
                        break
                row["key_count"] = len(result_keyword)
                keywordone.append(row)
                update_key_word(keywordone)
                LOGGER.info ('KEY:' + keyword + '('+str(row["key_count"])+') ')
        except Exception as e:
            LOGGER.info("--------------KEYWORD ERROR:" + str(row_count) + "------------{}".format(e))
            LOGGER.exception(e)


def google_search_for_bigkey():
    postfix = open('./config/postfix', 'r')
    postfixStr = postfix.readline()
    keywords = open('./Google/bigkey', 'r')
    for keyword in keywords:
        keyword = keyword.strip()
        num = 400
        results_per_page = 100
        if num % results_per_page == 0:
            pages = num / results_per_page
        else:
            pages = num / results_per_page + 1

        for p in range(0, pages):
            start = p * results_per_page
            get_url_sleep_time = random.randint(2, 5)
            result_keyword_one, result_num = mg.search(query=keyword + postfixStr, num=results_per_page,
                                                       language='en', start=start,
                                                       pause=get_url_sleep_time, keyword=keyword)
            insert_mysql(result_keyword_one, "listing_google_us")
            time.sleep(get_url_sleep_time)
            if result_num < start + 100:
                break


def update_key_word(keywords):
    update_sql = "UPDATE key_word_us set key_state = %s,key_count = %s  where key_word = %s"
    datas = []
    try:
        for i in keywords:
            data = (i["key_state"], i["key_count"], i["key_word"])
            datas.append(data)
    except Exception as e:
        LOGGER.info("Splicing UPDATE key_word_us data errors:{}".format(e))
    try:
        with mysql() as cursor:
            row_count = cursor.executemany(update_sql, datas)
    except Exception as e:
        LOGGER.info("UPDATE key_word_us errors" + keywords + ":{}".format(e) )


def google_search_for_brand_all():
    google_search_for_brand('title')
    google_search_for_brand('url')
    google_search_for_brand('search')


def google_search_for_brand(keytype):
    postfix = open('./config/postfix', 'r')
    postfix = postfix.readline()

    with mysql() as cursor:
        try:
            sql = "SELECT key_word,key_" + keytype + " from key_brand where key_" + keytype + " = 0 ORDER BY key_utime desc"
            row_count = cursor.execute(sql)
            LOGGER.info("-------------ALL Brand " + keytype + ":" + str(row_count) + "---------------")
            for row in cursor.fetchall():
                keywordone = []
                keyword = row["key_word"]
                # Total data number
                num = 400
                results_per_page = 100
                if num % results_per_page == 0:
                    pages = num / results_per_page
                else:
                    pages = num / results_per_page + 1

                result_keyword = []
                if keytype == 'search':
                    query = keyword + postfix
                else:
                    query = postfix + ' in' + keytype + ':' + keyword

                for p in range(0, pages):
                    start = p * results_per_page
                    get_url_sleep_time = random.randint(2, 5)
                    result_keyword_one, result_num = mg.search(query=query, num=results_per_page,
                                                               language='en', start=start,
                                                               pause=get_url_sleep_time, keyword=keyword,
                                                               keytype=keytype)
                    result_keyword = result_keyword + result_keyword_one
                    insert_mysql(result_keyword_one, "listing_google_us")
                    LOGGER.info('Stop some time:' + str(get_url_sleep_time))
                    time.sleep(get_url_sleep_time)
                    if result_num < start + 100:
                        break

                row[keytype] = len(result_keyword)
                keywordone.append(row)
                update_key_brand(keywordone, keytype)
        except Exception as e:
            LOGGER.info("-----------------------KEYWORD ERROR:" + str(row_count) + "---------------------{}".format(e))
            LOGGER.exception(e)


def update_key_brand(keywords, keytype):
    update_sql = "UPDATE key_brand set key_"+keytype+" = 1, key_"+keytype+"_count = %s where key_word = %s"
    datas = []
    try:
        for i in keywords:
            data = (i[keytype], i["key_word"])
            datas.append(data)
    except Exception as e:
        LOGGER.info("Splicing UPDATE key_brand data errors:{}".format(e))
    try:
        with mysql() as cursor:
            row_count = cursor.executemany(update_sql, datas)
            LOGGER.info("UPDATE key_brand {}/{} success:", row_count, len(keywords))
    except Exception as e:
        LOGGER.info("UPDATE key_brand errors:{}".format(e), keywords)


google_search()
