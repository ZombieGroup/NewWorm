# -*- coding: utf-8 -*-
from ScrollLoader import ScrollLoader
import re
import html2text
from bs4 import BeautifulSoup

from __init__ import get_xsrf
from Requests import requests

__author__ = 'ZombieGroup'
# 从Question url指向页面中抓取信息


class Question:

    def __init__(self, url):
        if not (re.match("http://www.zhihu.com/question/.+", url) or re.match("https://www.zhihu.com/question/.+", url)):
            raise ValueError("\"" + url + "\"" + " : it isn't a question url.")
        else:
            self.url = url
        self.title = None
        self.parser()

    def parser(self):
        try:
            r = requests.get(self.url)
            self.soup = BeautifulSoup(r.content)
        except:
            self.parser()

    def get_question_id(self):
        return self.url[len(self.url) - 8:len(self.url)]

    def get_follower_num(self):
        soup = self.soup
        followers_num = 0
        try:
            followers_num = int(
                soup.find("div", class_="zg-gray-normal").a.strong.string)
        except:
            pass
        finally:
            return followers_num

    def get_title(self):
        soup = self.soup
        title = soup.find(
            "h2", class_="zm-item-title").string.encode("utf-8").replace("\n", "")
        self.title = title
        return title

    def get_detail(self):
        soup = self.soup
        detail = str(soup.find("div", id="zh-question-detail").div)
        detail = html2text.html2text(detail)
        return detail

    def get_answer_num(self):
        soup = self.soup
        answer_num = 0
        try:
            answer_num = int(soup.find("h3", id="zh-question-answer-num")["data-num"])
        except:
            pass
        finally:
            return answer_num

    def get_edit_time(self):
        url = self.url + "/log"
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        logs = soup.find_all("div",class_="zm-item")
        timelist = []
        for log in logs:
            timelist.append(log.find("time").string)
        timelist.sort()
        return timelist

    def get_topics(self):
        soup = self.soup
        topic_tags = soup.find_all("a", class_="zm-item-tag")
        from Topic import Topic
        for topic_tag in topic_tags:
            topic_name = topic_tag.string
            topic_url = "http://www.zhihu.com" + topic_tag["href"]
            yield Topic(topic_url, topic_name)

    def get_answers(self):
        soup = self.soup
        answer_tags = soup.find_all("div", class_="zm-item-answer")
        from Answer import Answer
        for answer_tag in answer_tags:
            answer_url = self.url + "/answer/" + answer_tag["data-atoken"]
            yield Answer(answer_url)

    def get_followers(self):
        url = self.url + '/followers'
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        _xsrf = get_xsrf(soup)
        text = r.text
        scroll_loader = ScrollLoader("post", url, 20, _xsrf=_xsrf, start=0)
        for response in scroll_loader.run():
            for each in response:
                text += each
        user_list = re.findall(
            r'<a[^>]*\nclass=\"zm-item-link-avatar\"\nhref=\"([^>]*)\">', text)
        from User import User
        for url in user_list:
            user_url = "http://www.zhihu.com" + url
            #if not userBloom.is_element_exist(user_url):
            #    userBloom.insert_element(user_url)
            yield User(user_url)

    def get_data_resourceid(self):
        soup = self.soup
        return soup.find("div", class_="zm-item-rich-text js-collapse-body")['data-resourceid']

    def get_comments(self):
        url = "http://www.zhihu.com/node/QuestionCommentBoxV2?params={" + "\"question_id\":{0}".format(
            self.get_data_resourceid()) + "}"
        print url
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        for comment_div in soup.find_all("div", class_="zm-item-comment"):
            author_url = comment_div.find("a", class_="zg-link")['href']
            content = comment_div.find(
                "div", class_="zm-comment-content").next_element
            date = comment_div.find("span", class_="date").next_element
            like_num = comment_div.find(
                "span", class_="like-num ").next_element
            # Comment(author_url,question_url,answer_url,content,date,like_num)
            from Comment import Comment
            # TODO: comment bloom
            yield Comment(author_url, self.url, None, content, date, like_num)
