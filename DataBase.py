# -*- coding: utf-8 -*-_
_author__ = 'ZombieGroup'

import MySQLdb


class DataBase:

    def __init__(self, user=None, host=None, password=None, dbname=None):
        self.connect = MySQLdb.connect(
            host, user, password, dbname, port=3306, charset='utf8')

    def put_user_in_db(self, user):
        connect = self.connect
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
        following_topic_num = user.get_following_topic_num()
        following_column_num = user.get_following_column_num()

        value = (
            user_id, follower_num, followee_num, vote_num, thanks_num, ask_num, answer_num, article_num, collection_num,
            following_topic_num, following_column_num, education, education_extra, location, business, position,
            employment)
        if cursor.execute('select * from Users where user_ID="%s"' % user_id) is None:
            cursor.execute(
                '''insert into Users values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', value)
        cursor.close()
        connect.commit()
        connect.close()

    def put_follow_user_in_db(self, user):
        connect = self.connect
        cursor = connect.cursor()

        for follower in user.get_followers():
            follower_id = follower.get_user_id()
            if cursor.execute('''select user_ID from users where user_ID=%s''' % follower_id) is None:
                self.put_user_in_db(follower)
            elif cursor.execute('''select * from users where follower_ID=%s and followee_ID=%s''',
                                (follower_id, user.get_user_id())) is None:
                cursor.execute(
                    '''insert into follow_user values (%s, %s)''', (follower_id, user.get_user_id()))

        cursor.close()
        connect.commit()
        connect.close()

    def put_user_ask_in_db(self, user):
        connect = self.connect
        cursor = connect.cursor()

        for question in user.get_asks():
            question_id = question.get_question_id()
            if cursor.execute('''select * from questions where question_ID=%s''' % question_id) is None:
                self.put_question_in_db(question)
            cursor.execute('''update questions set asker_ID=%s where question_ID=%s''',
                           (user.get_user_id(), question_id))

        cursor.close()
        connect.commit()
        connect.close()

    def put_user_answer_in_db(self, user):
        connect = self.connect
        cursor = connect.cursor()

        for answer in user.get_answers():
            answer_id = answer.get_answer_id()
            if cursor.execute('select * from answers where answer_ID=%s' % answer_id) is None:
                self.put_answer_in_db(answer)
            elif cursor.fetchone(
                    'select author_ID from answers where answer_ID=%s' % answer_id) is not user.get_user_id():
                cursor.execute(
                    'update answers set author_ID=%s where answer_ID=%s', (user.get_user_id(), answer_id))

        cursor.close()
        connect.commit()
        connect.close()

    def put_question_in_db(self, question):
        connect = self.connect
        cursor = connect.cursor()

        question_id = question.get_question_id()
        asker_id = None
        detail = question.get_detail()
        title = question.get_title()
        answer_num = question.get_answer_num()
        follower_num = question.get_follower_num()

        values = (question_id, asker_id, detail,
                  title, answer_num, follower_num)

        if cursor.execute('select * from questions where question_ID=%s' % question_id) is None:
            cursor.excute(
                'insert into questions values (%s,%s,%s,%s,%s,%s)', values)

        cursor.close()
        connect.commit()
        connect.close()

    def put_answer_in_db(self, answer):
        connect = self.connect
        cursor = connect.cursor()
        cursor.close()

        answer_id = answer.get_answer_id()
        question_id = answer.get_question_id()
        author_id = answer.get_author_id()
        detail = answer.get_detail()
        upvote_num = answer.get_upvote_num()
        visited_times = answer.get_visited_times()

        values = (answer_id, question_id, author_id,
                  detail, upvote_num, visited_times)

        if cursor.execute('select * from answers where answer_ID=%s' % answer_id) is None:
            cursor.execute(
                'insert into answers values(%s,%s,%s,%s,%s,%s)', values)

        connect.commit()
        connect.close()

    def alter_user_in_db(self, field, detail, user_id):
        connect = self.connect
        cursor = connect.cursor()

        cursor.execute('update users set %s=%s where user_id=%s',
                       (field, detail, user_id))

        cursor.close()
        connect.commit()
        connect.close()
