# -*- coding: utf-8 -*-_
import MySQLdb
import re

import Logging
from Exceptions import *

__author__ = 'ZombieGroup'


class DataBase:
    connect = MySQLdb.connect('localhost', 'root', '', 'zhihu', port = 3306, charset = 'utf8')

    def __init__(self, user=None, host=None, password=None, dbname=None):
        self.connect = MySQLdb.connect(host, user, password, dbname, port = 3306, charset = 'utf8')

    @classmethod
    def put_user_in_db(cls, user):
        # if not userBloom.is_element_exist(user):
        connect = cls.connect
        cursor = connect.cursor()

        user_id = user.get_user_id()
        location = user.get_location()
        business = user.get_business()
        employment = user.get_employment()
        position = user.get_position()
        education = user.get_education()
        education_extra = user.get_education_extra()

        follower_num = user.get_follower_num()
        followee_num = user.get_followee_num()
        thanks_num = user.get_thanks_num()
        vote_num = user.get_vote_num()
        ask_num = user.get_ask_num()
        answer_num = user.get_answer_num()
        article_num = user.get_articles_num()
        collection_num = user.get_collection_num()
        following_topic_num, following_column_num = user.get_following_topic_colum_num()

        value = (
            user_id, follower_num, followee_num, vote_num, thanks_num, ask_num, answer_num, article_num, collection_num,
            following_topic_num, following_column_num, education, education_extra, location, business, position,
            employment)

        try:
            cursor.execute('insert into Users(user_id, followers_num, followees_num, agrees_num, thanks_num, asks_num, '
                           'answers_num, articles_num, collections_num, following_topics_num, following_columns, '
                           'education, education_extra, location, business, position, employment)'
                           ' values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', value)
        except MySQLdb.Error, e:
            if re.match(r'\(1062', str(e)):
                Logging.info(str(e))
        finally:
            connect.commit()

    @classmethod
    def put_follow_user_in_db(cls, user, follower):
        connect = cls.connect
        cursor = connect.cursor()

        user_id = user.get_user_id()
        follower_id = follower.get_user_id()
        value = (user_id, follower_id)

        try:
            cursor.execute('insert into Follow_User(follower_id, followee_id) values (%s, %s)', value)
        except MySQLdb.Error, e:
            if re.match(r'\(1062', str(e)):
                Logging.info(str(e))
        finally:
            connect.commit()

    @classmethod
    def put_follow_topic_in_db(cls, user, topic):
        connect = cls.connect
        cursor = connect.cursor()

        user_id = user.get_user_id()
        topic_id = topic.get_topic_id()
        value = (user_id, topic_id)
        try:
            cursor.execute('insert into Follow_Topic(follower_id, topic_id) values (%s,%s)', value)
        except MySQLdb.Error, e:
            if re.match(r'\(1062', str(e)):
                Logging.info(str(e))
        finally:
            connect.commit()

    @classmethod
    def put_follow_column_in_db(cls, user, column):
        connect = cls.connect
        cursor = connect.cursor()

        user_id = user.get_user_id()
        column_id = column.get_column_name()
        tmp = (user_id, column_id)
        try:
            cursor.execute('insert into Follow_Column(follower_id, column_name) values (%s,%s)', tmp)
        except MySQLdb.Error, e:
            if re.match(r'\(1062', str(e)):
                Logging.info(str(e))
        finally:
            connect.commit()

    @classmethod
    def put_follow_question_in_db(cls, question, user):
        connect = cls.connect
        cursor = connect.cursor()

        question_id = question.get_question_id()
        user_id = user.get_user_id()
        value = (question_id, user_id)
        try:
            cursor.execute('insert into Follow_Question(question_id, follower_id) values (%s,%s)', value)
        except MySQLdb.Error, e:
            if re.match(r'\(1062', str(e)):
                Logging.info(str(e))
        finally:
            connect.commit()

    @classmethod
    def put_user_ask_in_db(cls, user, question):
        connect = cls.connect
        cursor = connect.cursor()

        question_id = question.get_question_id()
        try:
            #cls.put_question_in_db(question)
            cursor.execute('update Questions set asker_id=%s where question_id=%s',
                               (user.get_user_id(), question_id))
        except MySQLdb.Error, e:
            if re.match(r'\(1062', str(e)):
                Logging.info(str(e))
        finally:
            connect.commit()

    @classmethod
    def put_user_answer_in_db(cls, user, answer):
        connect = cls.connect
        cursor = connect.cursor()

        answer_id = answer.get_answer_id()
        #cls.put_answer_in_db(answer)
        try:
            cursor.execute('update Answers set author_id=%s where answer_id=%s', (user.get_user_id(), answer_id))
        except MySQLdb.Error, e:
            if re.match(r'\(1062', str(e)):
                Logging.info(str(e))
        finally:
            connect.commit()

    @classmethod
    def put_question_in_db(cls, question):
        # if not questionBloom.is_element_exist(question):
        connect = cls.connect
        cursor = connect.cursor()

        question_id = question.get_question_id()
        asker_id = None
        detail = question.get_detail()
        title = question.get_title()
        answer_num = question.get_answer_num()
        follower_num = question.get_follower_num()
        time = question.get_edit_time()[0]
        values = (question_id, asker_id, detail, title, answer_num, follower_num,time)
        try:
            cursor.execute('insert into Questions(question_id, asker_id, detail, title, answers_num, '
                           'followers_num, post_time)'
                           ' values (%s,%s,%s,%s,%s,%s,%s)', values)
        except MySQLdb.Error, e:
            if re.match(r'\(1062', str(e)):
                Logging.info(str(e))
        finally:
            connect.commit()

    @classmethod
    def put_answer_in_db(cls, answer):
        connect = cls.connect
        cursor = connect.cursor()

        answer_id = answer.get_answer_id()
        question_id = answer.get_question_id()
        author_id = answer.get_author_id()
        detail = answer.get_detail()
        upvote_num = answer.get_upvote_num()
        visited_times = answer.get_visited_times()
        post_time = answer.get_post_time()
        last_update = answer.get_last_edit_time()

        values = (answer_id, question_id, author_id, detail, upvote_num, visited_times,post_time,last_update)
        try:
            cursor.execute('insert into Answers(answer_id, question_id, author_id, detail, upvote, '
                           'visit_times, post_time, last_edit_time) '
                           'values (%s,%s,%s,%s,%s,%s,%s,%s)', values)
        except MySQLdb.Error, e:
            if re.match(r'\(1062', str(e)):
                Logging.info(str(e))
        finally:
            connect.commit()

    @classmethod
    def put_topic_in_db(cls, topic):
        connect = cls.connect
        cursor = connect.cursor()

        topic_id = topic.get_topic_id()
        topic_name = topic.get_topic_name()
        question_num = topic.get_question_num()
        follower_num = topic.get_follower_num()
        #parent = topic.get_father()

        values = (topic_id, topic_name, question_num, follower_num)

        try:
            cursor.execute('insert into Topic(topic_id,topic_name,question_num,followers_num) '
                           'values (%s,%s,%s,%s)', values)
        except MySQLdb.Error, e:
            if re.match(r'\(1062', str(e)):
                Logging.info(str(e))
        finally:
            connect.commit()

    @classmethod
    def put_question_topic_in_db(cls, question, topic):
        connect = cls.connect
        cursor = connect.cursor()
        question_id = question.get_question_id()
        topic_id = topic.get_topic_id()
        values = (question_id, topic_id)
        try:
            cursor.execute('insert into Question_Topics(question_id, topic_id) values (%s,%s)', values)
        except MySQLdb.Error, e:
            if re.match(r'\(1062', str(e)):
                Logging.info(str(e))
        finally:
            connect.commit()

    @classmethod
    def put_column_in_db(cls, column):
        # if collumnBloom.is_element_exist(collumnBloom):
        connect = cls.connect
        cursor = connect.cursor()
        column_name = column.get_column_name()
        column_id = column.get_column_id()
        follower_num = column.getfollower_num()
        values = (column_id, column_name, follower_num)
        try:
            cursor.execute("insert into Columns(column_name, owner_id, follower_num) values (%s,%s,%s)", values)
        except MySQLdb.Error, e:
            if re.match(r'\(1062', str(e)):
                Logging.info(str(e))
        finally:
            connect.commit()

    @classmethod
    def put_article_in_db(cls, article):
        # if articleBloom.is_element_exist(article):
        connect = cls.connect
        cursor = connect.cursor()

        article_id = article.get_article_id()
        article_title = article.title
        comments_num = article.commentsCount
        column_name = article.column
        detail = article.content
        # TODO: Article.py 完善
        values = (article_id, column_name, comments_num, detail)
        try:
            cursor.execute('insert into Articles values (%s,%s,%s,%s)', values)
        except MySQLdb.Error, e:
            if re.match(r'\(1062', str(e)):
                Logging.info(str(e))
        finally:
            connect.commit()

    @classmethod
    def put_vote_in_db(cls, answer, voter):
        connect = cls.connect
        cursor = connect.cursor()

        answer_id = answer.get_answer_id()
        user_id = voter.get_user_id()
        values = (user_id, answer_id)
        try:
            cursor.execute('insert into Vote_Answer(voter_id, answer_id) values (%s,%s)', values)
        except MySQLdb.Error, e:
            if re.match(r'\(1062', str(e)):
                Logging.info(str(e))
        finally:
            connect.commit()
