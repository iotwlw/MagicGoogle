import os
import random
import sys

import cchardet
import re
import requests

reload(sys)
sys.setdefaultencoding('utf8')

from datetime import datetime
from pyquery import PyQuery as pq
from MagicBing.config import URL_NEXT, URL_FIRST, USER_AGENT, LOGGER

if sys.version_info[0] > 2:
    from urllib.parse import quote_plus, urlparse, parse_qs
else:
    from urllib import quote_plus
    from urlparse import urlparse, parse_qs


class MagicBing:
    """
    Magic google search.
    """

    def __init__(self, proxies=None):
        self.proxies = random.choice(proxies) if proxies else None

    def search(self, query, first=1, keyword=None):
        """
        Get the results you want,such as title,description,url

        :param first: 
        :type keyword: object
        :param keyword: 
        :param query:
        :return: Generator
        """
        content = self.search_page(query, first, keyword)
        self.content_to_html(content_html=content, log_prefix_name=keyword + '-' + str(first) + ' ')
        try:
            pq_content = self.pq_html(content)
        except Exception as e:
            print(keyword + str(first) + "-----------------------------------{}".format(e))
            return []
        else:
            if pq_content and '302 Moved' == pq_content('h1').eq(0).text():
                print(keyword + str(first) + "----------------------------------- Robot checked")
                return []
            else:
                result_dict_one = []
                for item in pq_content('li.b_algo').items():
                    title = item('div.b_title>h2>a').eq(0).text()
                    href = item('div.b_title>h2>a').eq(0).attr('href')
                    rating = ""
                    if item('div.b_vlist2col'):
                        rating = item('div.b_vlist2col').eq(0).text()
                        rating_out = re.search('\s(\d\.?\d?)/\d+\\n(\d+)', rating)
                        rating_out = rating_out.groups()
                        star = rating_out[0]
                        review = rating_out[1]
                    # ------------------------------------------Amazon--end--------------------
                    if href:
                        url = self.filter_link(href)

                    result_dict = {"title": title,
                                   "star": star,
                                   "review": review,
                                   "url": url,
                                   "rating": rating,
                                   }
                    result_dict_one.append(result_dict)
                return result_dict_one

    def search_page(self, query, first=1, keyword=None):
        """
        Google search
        :param keyword: 
        :param num: 
        :param first: 
        :param query: 
        :return: result
        """
        domain = "cn.bing.com"
        if first == 1:
            url = URL_FIRST
            url = url.format(
                domain=domain, query=quote_plus(query))
        else:
            url = URL_NEXT
            url = url.format(
                domain=domain, query=quote_plus(query), first=first)
        # Add headers
        headers = {'user-agent': self.get_random_user_agent()}
        try:
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
            r = requests.get(url=url,
                             # proxies=self.proxies,
                             headers=headers)
            LOGGER.info(url)
            content = r.content
            charset = cchardet.detect(content)
            text = content.decode(charset['encoding'])
            return text
        except Exception as e:
            LOGGER.exception(e)
            print(keyword + str(first) + "----------------------------------- Robot checked")
            return {}

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