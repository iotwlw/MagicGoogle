import os
import random
import sys
import time

import subprocess

import csv
import cchardet
import re
import requests
from requests.exceptions import SSLError

reload(sys)
sys.setdefaultencoding('utf8')

from datetime import datetime
from pyquery import PyQuery as pq
from MagicGoogle.config import USER_AGENT, DOMAIN, BLACK_DOMAIN, URL_SEARCH, URL_NEXT, URL_NUM, LOGGER

if sys.version_info[0] > 2:
    from urllib.parse import quote_plus, urlparse, parse_qs
else:
    from urllib import quote_plus
    from urlparse import urlparse, parse_qs


class MagicGoogle():
    """
    Magic google search.
    """

    def search(self, query, language=None, num=None, start=0, pause=2, keyword=None, keytype=None):
        """
        Get the results you want,such as title,description,url

        :param keyword: 
        :param keytype: 
        :param pause: 
        :param query:
        :param language:
        :param num:
        :param start:
        :return: Generator
        """
        content = self.search_page(query, language, num, start, pause, keyword)
        try:
            pq_content = self.pq_html(content)
        except Exception as e:
            print(keyword + str(start) + "-----------pq_html---------error---------------{}".format(e))
            return [], -1
        else:

            if pq_content and '302 Moved' == pq_content('h1').eq(0).text():
                try:
                    print(keyword + str(start) + "-------------- change proxy")
                    self.change_ip_for_vps()
                    content = self.search_page(query, language, num, start, pause, keyword)
                    pq_content = self.pq_html(content)
                except Exception as e:
                    print(keyword + str(start) + "------after change proxy error-------{}".format(e))
                    return [], -1

            try:
                result_num = pq_content('#resultStats')
                if result_num:
                    result_num = result_num.text()
                    result_num = re.search('bout\s(\d*,?\.?\d*,?\.?\d*,?\.?\d*) results', result_num)
                    if result_num:
                        result_num = result_num.group()
                        result_num = result_num.lstrip('bout ').rstrip(' results').replace(',', '').replace('.', '')
                        result_num = int(result_num)
                    else:
                        return [], 0
                else:
                    return [], 0
            except Exception as e:
                result_num = -1
                print(keyword + str(start) + "------------------result_num errors------------{}".format(e))

            result_dict_one = []
            for item in pq_content('div.g').items():
                asin = ""
                url = ""
                title = item('h3.r>a').eq(0).text()
                # ------------------------------------------Amazon--begin--------------------
                rating = item('div.f.slp').eq(0).text()
                if rating:
                    rating = rating.encode('utf-8')
                    rating = rating.replace("\xc2\xa0", "")
                    rating_out = rating.lstrip('Rating: ').rstrip(' reviews')
                    rating_out = rating_out.split('-')
                    star = rating_out[0].replace(',', '.')
                    review = rating_out[1].replace(',', '')
                else:
                    star = 0.0
                    review = 0
                # ------------------------------------------Amazon--end--------------------
                href = item('h3.r>a').eq(0).attr('href')
                if href:
                    url = self.filter_link(href)
                    if url:
                        asin = re.search('dp/(\w{10})', url)
                        if asin:
                            asin = asin.groups()[0]
                insert_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                insert_datetime = str(insert_datetime)

                result_dict = {
                    "asin": asin,
                    "insert_datetime": insert_datetime,
                    "url": url,
                    "title": title,
                    "review_num": review,
                    "review_value": star,
                    "keytype": keytype,
                    "keyword": keyword

                }
                result_dict_one.append(result_dict)
            return result_dict_one, result_num

    def search_page(self, query, language=None, num=None, start=0, pause=2, keyword=None):
        """
        Google search
        :param num: 
        :param start: 
        :param pause: 
        :param query: Keyword
        :param language: Language
        :return: result
        """
        domain = self.get_random_domain()
        if start > 0:
            url = URL_NEXT
            url = url.format(
                domain=domain, language=language, query=quote_plus(query), num=num, start=start)
        else:
            if num is None:
                url = URL_SEARCH
                url = url.format(
                    domain=domain, language=language, query=quote_plus(query))
            else:
                url = URL_NUM
                url = url.format(
                    domain=domain, language=language, query=quote_plus(query), num=num)
        if language is None:
            url = url.replace('hl=None&', '')
        # Add headers
        headers = {'user-agent': self.get_random_user_agent()}
        try:
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
            r = requests.get(url=url,
                             # proxies=self.proxies,
                             headers=headers,
                             allow_redirects=False,
                             verify=False,
                             timeout=30)
            content = r.content
            charset = cchardet.detect(content)
            text = content.decode(charset['encoding'])
            return text
        except SSLError as e:
            LOGGER.exception(e)
            LOGGER.info(url)
            return {}
        except Exception as e:
            LOGGER.exception(e)
            LOGGER.info(url)
            print(keyword + str(start) + "---------- change proxy for bad proxy -------------")
            self.change_ip_for_vps()
            return {}

    def search_url(self, query, language=None, num=None, start=0, pause=2):
        """
        :param query:
        :param language:
        :param num:
        :param start:
        :return: Generator
        """
        content = self.search_page(query, language, num, start, pause)
        pq_content = self.pq_html(content)
        for item in pq_content('h3.r').items():
            href = item('a').attr('href')
            if href:
                url = self.filter_link(href)
                if url:
                    yield url

    def filter_link(self, link):
        """
        Returns None if the link doesn't yield a valid result.
        Token from https://github.com/MarioVilas/google
        :return: a valid result
        """
        try:
            # Valid results are absolute URLs not pointing to a Google domain
            # like images.google.com or googleusercontent.com
            o = urlparse(link, 'http')
            if o.netloc:
                return link
            # Decode hidden URLs.
            if link.startswith('/url?'):
                link = parse_qs(o.query)['q'][0]
                # Valid results are absolute URLs not pointing to a Google domain
                # like images.google.com or googleusercontent.com
                o = urlparse(link, 'http')
                if o.netloc:
                    return link
        # Otherwise, or on error, return None.
        except Exception as e:
            LOGGER.exception(e)
            return None

    def pq_html(self, content):
        """
        Parsing HTML by pyquery
        :param content: HTML content
        :return:
        """
        return pq(content)

    def get_random_user_agent(self):
        """
        Get a random user agent string.
        :return: Random user agent string.
        """
        return random.choice(self.get_data('user_agents.txt', USER_AGENT))

    def get_random_domain(self):
        """
        Get a random domain.
        :return: Random user agent string.
        """
        # domain = random.choice(self.get_data('all_domain.txt', DOMAIN))
        domain = 'www.google.com'
        if domain in BLACK_DOMAIN:
            self.get_random_domain()
        else:
            return domain

    def get_data(self, filename, default=''):
        """
        Get data from a file
        :param filename: filename
        :param default: default value
        :return: data
        """
        root_folder = os.path.dirname(__file__)
        user_agents_file = os.path.join(
            os.path.join(root_folder, 'data'), filename)
        try:
            with open(user_agents_file) as fp:
                data = [_.strip() for _ in fp.readlines()]
        except:
            data = [default]
        return data

    def dict_list_to_csv_file(self, result_list, csv_prefix_name, headers):
        print("***********************************")
        print("start to write csv file...")
        if not headers:
            for i in result_list[0]:
                headers.append(i)

        csv_folder = "AmazonData"
        csv_data_time = str(datetime.now()).replace(":", ";").strip().split(".")[0]
        csv_file_path = csv_folder + "/" + csv_prefix_name + csv_data_time + ".csv"

        if not os.path.exists(csv_folder):
            print("***********************************")
            print("reviews folder not exist, create the folder now...")
            os.mkdir(csv_folder)
            print("success to create AmazonData folder")

        try:
            with open(csv_file_path, 'wb') as f:
                f_csv = csv.DictWriter(f, headers)
                f_csv.writeheader()
                f_csv.writerows(result_list)
                print("success to write csv file...")
        except Exception as e:
            print("fail to write csv!: {}".format(e))

    def content_to_html(self, content_html, log_prefix_name):
        print("-------------------------Save content to html--------------------------------")
        log_folder = "log"
        log_data_time = str(datetime.now()).replace(":", ";").strip().split(".")[0]
        log_file_path = log_folder + "/" + log_prefix_name + log_data_time + ".html"
        if not os.path.exists(log_folder):
            os.mkdir(log_folder)
        try:
            f = open(log_file_path, 'wb')
            f.write(content_html)
            f.close()
        except Exception as e:
            print("fail to write log!: {}".format(e))

    def change_ip_for_vps(self):
        try:
            subprocess.Popen('pppoe-stop', shell=True, stdout=subprocess.PIPE)
            time.sleep(2)
            subprocess.Popen('pppoe-start', shell=True, stdout=subprocess.PIPE)
            time.sleep(5)
            pppoe_restart = subprocess.Popen('pppoe-status', shell=True, stdout=subprocess.PIPE)
            pppoe_restart.wait()
            pppoe_log = pppoe_restart.communicate()[0]
            adsl_ip = re.findall(r'inet (.+?) peer ', pppoe_log)[0]
            print '[*] New ip address : ' + adsl_ip
            return True
        except Exception, e:
            print e
            self.change_ip_for_vps()